// webpack plugins
const CommonsChunkPlugin = require('webpack/lib/optimize/CommonsChunkPlugin');
const webpack = require('webpack');
const path = require('path');
const ngAnnotatePlugin = require('ng-annotate-webpack-plugin');
const LiveReloadPlugin = require('webpack-livereload-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
  devtool: 'source-map',
  entry: {
      "./designsafe/apps/rapid/static/designsafe/apps/rapid/build/bundle.js" : "./designsafe/apps/rapid/static/designsafe/apps/rapid/scripts/index.js",
  },
  output: {
    path: __dirname,
    filename: "[name]"
  },
  resolve: {
    extensions: ['.js'],
    modules: ['node_modules']
  },

  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
        options: {
          presets: ['es2015']
        }
      },
      {
        test: /\.(s?)css$/,
        use: ExtractTextPlugin.extract({
              fallback: "style-loader",
              use: [{ loader: 'css-loader',},
                    { loader: 'sass-loader',
                      options: { sourceMap: true,
                                 includePaths: ["./designsafe/static/styles"]
                               }
                    }]
            })
      },
    ]
  },
  plugins: [
    new ExtractTextPlugin("./designsafe/static/styles/base.css"),
    new ngAnnotatePlugin({add:true}),
    new LiveReloadPlugin(),
  ],

  externals: {
    jQuery: 'jQuery',
    $: 'jQuery',
    jquery: 'jQuery',
    Modernizr: 'Modernizr',
    angular: 'angular',
    d3: 'd3',
    moment: 'moment',
    _: '_',
    L: 'L',
    window: 'window',
  }
};
