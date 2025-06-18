import pandas as pd
import os
import json

class ExpensesProcesser:
    report_file_name = "report.json"

    def get_expenses(self, statement_data):
        all_expenses = statement_data[statement_data["Type"].str.strip() == "Expense"]["Value"]
        return all_expenses.tolist()

    def get_revenue(self, statement_data):
        all_revenue = statement_data[statement_data["Type"].str.strip() == "Income"]["Value"]
        return all_revenue.tolist()

    def calculate_total(self, values):
        total = 0
        for value in values:
            total += float(value)
        return total

    def get_net_revenue(self, total_expenses, total_revenue):
        return total_revenue-total_expenses

    def generate_expense_report_json(self, total_expenses, total_revenue, net_revenue):
        expense_report = {
            "gross-revenue": total_revenue,
            "expenses": total_expenses,
            "net-revenue": net_revenue
        }
        return expense_report

    def read_statement_data_from_file(self, file_name="data.csv"):
        column_names = ["Date", "Type", "Value", "Description"]
        df = pd.read_csv(
            file_name,
            header=None,
            names=column_names,
            comment='#',
            skipinitialspace=True
        )
        return df

    def write_report_to_server(self, file_data, file_name):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, file_name)

        with open(file_path, "w") as f:
            json.dump(file_data, f, indent=4)
        
        print("Written to server!")

    def write_csv_file_to_server(self, file_data, file_name):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, file_name)
        file_data.save(file_path)
        return file_path

    def get_report_from_server(self):
        script_directory = os.path.dirname(__file__)
        file_path = os.path.join(script_directory, self.report_file_name)
        with open(file_path, 'r') as file:
            return json.load(file)

    def process_report_async(self):
        statement_data = self.read_statement_data_from_file()
        expenses = self.get_expenses(statement_data)
        revenue = self.get_revenue(statement_data)

        total_expenses = self.calculate_total(expenses)
        total_revenue = self.calculate_total(revenue)
        net_revenue = self.get_net_revenue(total_expenses, total_revenue)

        json_formatted_report = self.generate_expense_report_json(total_expenses, total_revenue, net_revenue)
        self.write_report_to_server(json_formatted_report, "report.json")