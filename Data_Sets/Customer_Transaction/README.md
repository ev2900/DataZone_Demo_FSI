# Customer Transaction Data Set

## Overview
This data set represents a sample of transactional data for customers in the financial services industry. It is designed to demonstrate various types of transactions that a customer might undertake, including deposits, withdrawals, transfers, and loan payments. The data is useful for analyzing customer behavior, transaction patterns, and for financial modeling purposes.

## Data Description
The data set comprises the following columns:

1. **TransactionID**: A unique identifier for each transaction. It follows the format 'TX' followed by a number (e.g., TX1000).
2. **CustomerID**: A unique identifier for each customer. This is represented in the format 'CUST' followed by a number (e.g., CUST224). This ID links the transaction to a specific customer.
3. **TransactionDate**: The date on which the transaction occurred. The format is YYYY-MM-DD (e.g., 2022-10-05).
4. **TransactionType**: The type of transaction. This field can take one of the following values:
   - **Deposit**: Money added to the customer’s account.
   - **Withdrawal**: Money taken out of the customer’s account.
   - **Transfer**: Money moved either to another account of the same customer or to a different customer's account.
   - **Loan Payment**: Payment made by the customer against a loan.
5. **Amount**: The monetary value of the transaction. This is a floating-point number representing the transaction amount in the respective currency.
6. **Currency**: The currency in which the transaction was made. This field can include various currencies such as USD (US Dollar), EUR (Euro), GBP (British Pound), JPY (Japanese Yen), and AUD (Australian Dollar).

## Usage Notes
- This data set is intended for demonstration purposes in the context of financial services.
- Ensure that the data is used in compliance with data governance policies and privacy standards.
- The data is generated and does not correspond to real individuals or transactions.

## File Format
The data set is provided in CSV format, which can be imported into various data analysis tools and software.
