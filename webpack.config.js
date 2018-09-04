var path = require("path");
var webpack = require("webpack");
var BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  context: __dirname,
  mode: "development",
  entry: "./dangit-client/index",
  output: {
      path: path.resolve("./dangit-client/output/bundles/"),
      filename: "[name]-[hash].js"
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      }
    ]
  },
  plugins: [
    new BundleTracker({filename: "./dangit-client/output/webpack-stats.json"})
  ]
};
