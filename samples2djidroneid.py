#!/usr/bin/python3

import argparse
import subprocess

PROCESS_FILE = '/build/dji_droneid/matlab/updated_scripts/process_file.m'


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--samp-rate',
        help='sample rate of recording in samples/sec',
        default=15.36e6,
        type=float,
        choices=[15.36e6, 30.72e6],
    )
    parser.add_argument(
        '--center-offset',
        help='center frequency offset of DroneID signals in Hz',
        default=0e6,
        type=float,
    )
    parser.add_argument(
        'samples',
        help='filename of I/Q sample recording of DroneID signals (must be complex float)',
        type=str,
    )
    return parser


def run_process_file(args, process_file):
    process_file_args = ['octave-cli', process_file, args.samples, str(args.samp_rate), str(args.center_offset)]
    process_file_out = subprocess.run(process_file_args, capture_output=True)
    if process_file_out.returncode:
        raise ValueError(f'{process_file} failed to run: {process_file_out.stderr}')
    raw_frames = [frame for frame in process_file_out.stdout.decode('utf8').splitlines() if frame.startswith('FRAME')]
    print(raw_frames)


def main():
    parser = argument_parser()
    args = parser.parse_args()
    run_process_file(args, PROCESS_FILE)


if __name__ == '__main__':
    main()
