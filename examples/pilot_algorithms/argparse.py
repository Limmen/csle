from argparse import ArgumentParser, Namespace

parser = ArgumentParser()

parser.add_argument('square', help ='calculates square', type=int)
parser.add_argument('-v', '--verbose', help='verbose description', action='store true') 
args = parser.parse_args()

if args.verbose:
    print(f'{args.square} square is: {args.square ** 2}')
else:
    print(args.square ** 2)
    