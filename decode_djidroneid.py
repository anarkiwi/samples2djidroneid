#!/usr/bin/python3

import argparse
import json
import struct

# https://petapixel.com/assets/uploads/2022/08/Anatomy-of-DJI-Drone-ID-Implementation1.pdf

def int2deg(x):
  return x / 174533.0


# https://github.com/kismetwireless/kismet/blob/master/dot11_parsers/dot11_ie_221_dji_droneid.h
DRONEID_FIELDS = (
  ('framelen', 'B', int),
  ('msgtype', 'B', int),
  ('version', 'B', int),
  ('seqno', 'H', int),
  ('state_info', 'h', int),
  ('serial_no', '16s', lambda x: x.decode('utf8').strip('\x00')),
  ('longitude', 'i', int2deg),
  ('latitude', 'i', int2deg),
  ('height', 'H', int),
  ('altitude', 'H', int),
  ('velocity_north', 'h', int),
  ('velocity_east', 'h', int),
  ('velocity_up', 'h', int),
  ('yaw', 'h', lambda x: x / 100.0 / 57.296),
  ('phone_app_gps_time', 'Q', int), 
  ('phone_app_latitude', 'i', int2deg),
  ('phone_app_longitude', 'i', int2deg),
  ('home_latitude', 'i', int2deg),
  ('home_longitude', 'i', int2deg),
  ('product_type', 'B', int),
  ('uuid_length', 'B', int),
  ('uuid', '19s', lambda x: x.decode('utf8')),
  ('null', 'B', int),
  ('crc', 'h', int),
)


def decode(data):
    unpack_format = '<' + ''.join((field_type for _, field_type, _ in DRONEID_FIELDS))
    results = struct.unpack(unpack_format, data[:91])
    frame = {}
    for field_metadata, result in zip(DRONEID_FIELDS, results):
        field, _, field_decoder = field_metadata
        frame[field] = field_decoder(result)
    print(json.dumps(frame))


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'frames',
        help='filename of files containing a list of frames',
        type=str,
    )
    return parser


def main():
    parser = argument_parser()
    args = parser.parse_args()

    with open(args.frames, 'r') as f:
        for line in f:
            if line.startswith('FRAME'):
                data=bytearray(bytes.fromhex(line[7:].strip()))
                decode(data)


if __name__== '__main__':
    main()
