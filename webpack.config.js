const path = require('path');
const { VueLoaderPlugin } = require('vue-loader')
module.exports = {

  entry: [
    './static/index.js'
  ],
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'static/dist/'),
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        use: 'vue-loader'
      }
    ]
  },
  plugins: [
    new VueLoaderPlugin()
  ]
}