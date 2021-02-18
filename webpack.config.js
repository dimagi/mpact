const path = require('path');
const { VueLoaderPlugin } = require('vue-loader')
module.exports = {
  entry: [
    './static/main.js'
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
      },
      {
        test: /\.css$/i,
        use: ["style-loader","css-loader"],
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
      },
    ]
  },
  resolve: {
    alias: {
      vue: 'vue/dist/vue.js'
    }
  },
  plugins: [
    new VueLoaderPlugin()
  ]
}