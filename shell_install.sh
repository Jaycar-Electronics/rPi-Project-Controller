#!/bin/bash


PITFT_VALUES=(pitft22 pitft28-resistive pitft28-capacitive pitft35-resistive)
WIDTH_VALUES=(320 320 320 480)
HEIGHT_VALUES=(240 240 240 320)
HZ_VALUES=(80000000 80000000 80000000 32000000)
# Framebuffer (HDMI out) rotation:
FBROTATE_VALUES=(0 1 2 3)
# PiTFT (MADCTL) rotation:
TFTROTATE_VALUES=(0 90 180 270)

echo
echo "Select display type:"
#        123456789012345678901234567890123456789
selectN "PiTFT 2.2\" HAT" \
	"PiTFT / PiTFT Plus resistive 2.4-3.2\"" \
	"PiTFT / PiTFT Plus 2.8\" capacitive" \
	"PiTFT / PiTFT Plus 3.5\""
PITFT_SELECT=$?

echo
echo "HDMI rotation:"
selectN "Normal (landscape)" \
	"90° clockwise (portrait)" \
	"180° (landscape)" \
	"90° counterclockwise (portrait)"
FBROTATE_SELECT=$?

echo
echo "TFT (MADCTL) rotation:"
selectN "0" \
	"90" \
	"180" \
	"270"
TFTROTATE_SELECT=$?


echo "Device: ${PITFT_VALUES[$PITFT_SELECT-1]}"
echo "HDMI framebuffer rotate: ${FBROTATE_VALUES[$FBROTATE_SELECT-1]}"
echo "TFT MADCTL rotate: ${TFTROTATE_VALUES[$TFTROTATE_SELECT-1]}"
echo


