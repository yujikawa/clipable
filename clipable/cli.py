import pandas as pd
import pyperclip
import argparse
import io
import pytablewriter


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
        
        data.fillna('', inplace=True)
        writer = pytablewriter.MarkdownTableWriter()
        writer.from_dataframe(data)
        md = writer.dumps()

        print(md)
        print('......Succeeded!!')
        pyperclip.copy(md)

    except Exception as e:
        print('Error: cannot clipboard to markdown. Please check your clipboard')


if __name__ == '__main__':
    main()
