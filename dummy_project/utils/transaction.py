from lib.activity import Activity


class Transaction(Activity):
    def __enter__(self):
        print('Transaction started')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Transaction ended')
