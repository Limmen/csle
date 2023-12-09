from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument('square', help ='calculates square', type=int)
parser.add_argument('-v', '--verbose', help='verbose description', action='store_true') 
args = parser.parse_args()

print(args.verbose)
if args.verbose:
    print(f'{args.square} square is: {args.square ** 2}')
else:
    print(args.square ** 2)
    