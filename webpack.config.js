var path = require("path");
var process = require("process");
var webpack = require("webpack");
var BundleTracker = require("webpack-bundle-tracker");

const devtool = process.env["NODE_ENV"] === "production" ? "source-map" : "inline-source-map";

module.exports = {
  context: __dirname,
  mode: process.env["NODE_ENV"] || "development",
  entry: "./dangit-client/index",
  devtool: devtool,
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
      },
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/
      }
    ]
  },
  resolve: {
    extensions: [ '.tsx', '.ts', '.js' ]
  },
  plugins: [
    new BundleTracker({filename: "./dangit-client/output/webpack-stats.json"})
  ]
};
