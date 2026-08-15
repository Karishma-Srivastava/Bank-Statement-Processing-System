import os


def export_csv(df, output_path):
    """
    Export transactions to CSV.
    """

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    df.to_csv(
        output_path,
        index=False
    )

    return output_path


def export_excel(df, output_path):
    """
    Export transactions to Excel.
    """

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    df.to_excel(
        output_path,
        index=False
    )

    return output_path