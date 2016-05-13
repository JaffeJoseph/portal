from django.conf import settings
from elasticsearch_dsl import Search, DocType
from elasticsearch_dsl.query import Q
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.utils import AttrList
from elasticsearch import TransportError
from designsafe.apps.api.data.agave.file import AgaveFile
import dateutil.parser
import datetime
import logging
import six
import re
import os

logger = logging.getLogger(__name__)

es_settings = getattr(settings, 'ELASTIC_SEARCH', {})

try:
    default_index = es_settings['default_index']
    cluster = es_settings['cluster']
    hosts = cluster['hosts']
except KeyError as e:
    logger.exception('ELASTIC_SEARCH missing %s' % e)

connections.configure(
    default={
        'hosts': hosts,
        'sniff_on_start': True,
        'sniff_on_connection_fail': True,
        'sniffer_timeout': 60,
        'retry_on_timeout': True,
        'timeout:': 20,
    })

class Object(DocType):
    source = 'agave'

    @classmethod
    def listing(cls, system, username, file_path):
        q = {"query":{"filtered":{"query":{"bool":{"must":[{"term":{"path._exact":file_path}}, {"term": {"systemId": system}}]}},"filter":{"bool":{"should":[{"term":{"owner":username}},{"terms":{"permissions.username":[username, "world"]}}], "must_not":{"term":{"deleted":"true"}} }}}}}
        s = cls.search()
        s.update_from_dict(q)
        return cls._execute_search(s)

    @classmethod
    def from_file_path(cls, system, username, file_path):
        path, name = os.path.split(file_path)
        path = path or '/'
        q = {"query":{"filtered":{"query":{"bool":{"must":[{"term":{"path._exact":path}},{"term":{"name._exact":name}}, {"term": {"systemId": system}}]}},"filter":{"bool":{"must_not":{"term":{"deleted":"true"}}}}}}}
        if username is not None:
            q['query']['filtered']['filter']['bool']['should'] = [{"term":{"owner":username}},{"terms":{"permissions.username":[username, "world"]}}] 

        s = cls.search()
        s.update_from_dict(q)
        res, s = cls._execute_search(s)
        if res.hits.total:
            return res[0]
        else:
            return None

    @classmethod
    def listing_recursive(cls, system, username, file_path):
        q = {"query":{"filtered":{"query":{"bool":{"must":[{"term":{"path._path":file_path}}, {"term": {"systemId": system}}]}},"filter":{"bool":{"should":[{"term":{"owner":username}},{"terms":{"permissions.username":[username, "world"]}}], "must_not":{"term":{"deleted":"true"}} }}}}}
        s = cls.search()
        s.update_from_dict(q)
        return cls._execute_search(s)

    @classmethod
    def from_agave_file(cls, username, file_obj, auto_update = False, get_pems = False):
        o = cls.from_file_path(file_obj.system, username, file_obj.full_path)
        if o is not None:
            if auto_update:
                o.update(
                    mimeType = file_obj.mime_type,
                    name = file_obj.name,
                    format = file_obj.format,
                    deleted = False,
                    lastModified = file_obj.lastModified.isoformat(),
                    fileType = file_obj.ext or 'folder',
                    agavePath = 'agave://{}/{}'.format(file_obj.system, file_obj.full_path),
                    systemTags = [],
                    length = file_obj.length,
                    systemId = file_obj.system,
                    path = file_obj.parent_path,
                    keywords = [],
                    link = file_obj._links['self']['href'],
                    type = file_obj.type
                )
            if get_pems:
                o.update(permissions = file_obj.permissions)
            return o

        o = cls(
            mimeType = file_obj.mime_type,
            name = file_obj.name,
            format = file_obj.format,
            deleted = False,
            lastModified = file_obj.lastModified.isoformat(),
            fileType = file_obj.ext or 'folder',
            agavePath = 'agave://{}/{}'.format(file_obj.system, file_obj.full_path),
            systemTags = [],
            length = file_obj.length,
            systemId = file_obj.system,
            path = file_obj.parent_path,
            keywords = [],
            link = file_obj._links['self']['href'],
            type = file_obj.type
        )
        o.save()
        if get_pems:
            pems = file_obj.permissions
        else:
            path = file_obj.path
            pems_user = path.strip('/').split('/')[0]
            pems [{
                'username': pems_user,
                'recursive': True,
                'permission': {
                    'read': True,
                    'write': True,
                    'execute': True
                }
            }]

        o.update(permissions = pems)
        return o

    @staticmethod        
    def _execute_search(s):
        try:
            res = s.execute()
        except TransportError as e:
            if e.status_code == 404:
                raise
            res = s.execute()
        return res, s

    def copy(self, username, path):
        #split path arg. Assuming is in the form /file/to/new_name.txt
        tail, head = os.path.split(path)
        #check if we have something in tail.
        #If we don't then we got just the new file name in the path arg.
        if tail == '':
            head = path
        if self.type == 'dir':
            res, s = self.__class__.listing_recursive(self.system, username, os.path.join(self.path, self.name))
            for o in s.scan():
                d = o.to_dict()
                regex = r'^{}'.format(os.path.join(self.path, self.name))
                d['path'] = re.sub(regex, os.path.join(self.path, head), d['path'], count = 1)
                d['agavePath'] = 'agave://{}/{}'.format(self.systemId, os.path.join(d['path'], d['name']))
                doc = Object(**d)
                doc.save()
        d = self.to_dict()
        d['name'] = head
        d['agavePath'] = 'agave://{}/{}'.format(self.systemId, os.path.join(d['path'], d['name']))
        doc = Object(**d)
        doc.save()
        self.save()
        return self

    def delete_recursive(self):
        cnt = 0
        if self.type == 'dir':
            res, s = self.__class__.listing_recursive(self.system, username, os.path.join(self.path, self.name))
            for o in s.scan():
                o.delete()
                cnt += 1

        self.delete()
        cnt += 1
        return cnt

    def move(self, username, path):
        if self.type == 'dir':
            res, s = self.__class__.listing_recursive(self.system, username, os.path.join(self.path, self.name))
            for o in s.scan():
                regex = r'^{}'.format(os.path.join(self.path, self.name))
                o.update(path = re.sub(regex, os.path.join(path, self.name), o.path, count = 1))
                o.update(agavePath = 'agave://{}/{}'.format(self.systemId, os.path.join(self.path, self.name))) 

        tail, head = os.path.split(path)
        self.update(path = tail)
        self.update(agavePath = 'agave://{}/{}'.format(self.systemId, os.path.join(self.path, self.name)))
        logger.debug('Moved: {}'.format(self.to_dict()))
        self.save()
        return self


    def rename(self, username, path):
        #split path arg. Assuming is in the form /file/to/new_name.txt
        tail, head = os.path.split(path)
        #check if we have something in tail.
        #If we don't then we got just the new file name in the path arg.
        if tail == '':
            head = path       
        if self.type == 'dir':
            res, s = self.__class__.listing_recursive(self.system, username, os.path.join(self.path, self.name))
            for o in s.scan():
                regex = r'^{}'.format(os.path.join(self.path, self.name))
                o.update(path = re.sub(regex, os.path.join(self.path, head), o.path, count = 1))
                o.update(agavePath = 'agave://{}/{}'.format(self.systemId, os.path.join(self.path, head)))
                logger.debug('Updated document to {}'.format(os.path.join(o.path, o.name)))
        self.update(name = head)
        self.update(agavePath = 'agave://{}/{}'.format(self.systemId, os.path.join(self.path, head)))
        logger.debug('Updated ocument to {}'.format(os.path.join(self.path, self.name)))
        self.save()
        return self

    def share(self, username, user_to_share, permission):
        if self.type == 'dir':
            res, s = self.__class__.listing_recursive(self.system, username, os.path.join(self.path, self.naem))
            for o in s.scan():
                o.update_pems(user_to_share, permission)
        
        path_comps = os.path.join(self.path, self.name).split('/')
        path_comps.pop()
        for i in range(len(path_comps)):
            doc_path = '.'.join(path_comps)
            doc = Object.from_file_path(self.systemId, username, doc_path)
            doc.update_pems(user_to_share, permission)
            path_comps.pop()

        self.update_pems(user_to_share, permission)
        self.save()
        return self

    def update_pems(self, user_to_share, pem):
        pems = getattr(self, 'permissions', [])
        pem_to_add = {
                'username': user_to_share,
                'recursive': True,
                'permission': {
                    'read': True if pem in ['READ', 'ALL'] else False,
                    'write': True if pem in ['WRITE', 'ALL'] else False,
                    'execute': True if pem in ['EXECUTE', 'ALL'] else False
                }
            }
        user_pems = filter(lambda x: x['username'] != user_to_share, pems)
        user_pems.append(pem_to_add)
        self.update(permissions = user_pems)
        self.save()
        return self
        
    def to_file_dict(self):
        try:
            lm = dateutil.parser.parse(self.lastModified)
        except AttributeError:
            lm = datetime.datetime.now()

        wrap = {
            'format': getattr(self, 'format', 'folder'),
            'lastModified': lm,
            'length': self.length,
            'mimeType': self.mimeType,
            'name': self.name,
            'path': os.path.join(self.path, self.name).strip('/'),
            'permissions': self.permissions,
            'system': self.systemId,
            'type': self.type,
            '_permissions': self.permissions
        }
        f = AgaveFile(wrap = wrap)
        return f.to_dict()

    class Meta:
        index = default_index
        doc_type = 'objects'
