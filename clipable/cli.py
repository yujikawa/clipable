import pandas as pd
import pyperclip
import argparse
import io


def main():
    parser = argparse.ArgumentParser(
        description='Your clipboard(Excel or Google spreadsheet) change to markdown clipboard',
        add_help=True,
    )
    parser.add_argument('-f', help='Please input format type(csv)', default=None, type=str)

    try:

        args = parser.parse_args()
        if args.f is None:
            data = pd.read_clipboard()
        elif args.f == 'csv':
            data = pd.read_csv(io.StringIO(pyperclip.paste()))
        elif args.f == 'tsv':
            data = pd.read_csv(io.StringIO(pyperclip.paste()), sep="\t")

        print(data.head(3).to_markdown())
        print('......Succeeded!!')
        pyperclip.copy(data.to_markdown())

    except Exception as e:
        print('Error: cannot clipboard to markdown. Please check your clipboard')


if __name__ == '__main__':
    main()
