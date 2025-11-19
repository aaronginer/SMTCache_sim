#!/bin/bash

# benchmarking mail only works within local network for now

echo "Running streaming-server benchmark with timeout=${2} and IP=${1}..."

timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test1.mkv &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test1.mkv &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test1.mkv &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test1.mkv &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test1.mkv &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test1.mkv &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test1.mkv &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test1.mkv &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test1.mkv &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test1.mkv &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test2.mp3 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test2.mp3 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test2.mp3 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test2.mp3 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test2.mp3 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test2.mp3 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test2.mp3 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test2.mp3 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test2.mp3 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test2.mp3 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test2.mp3 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test3.mp4 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test3.mp4 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test3.mp4 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test3.mp4 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test3.mp4 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test3.mp4 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test3.mp4 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test3.mp4 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test3.mp4 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test3.mp4 &
timeout -k 1s ${2}s openRTSP rtsp://${1}:7654/test3.mp4 &

wait