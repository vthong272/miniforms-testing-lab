# MiniForms — Golden Business Rules

These rules define the expected behavior of the golden version. Test suites must be designed from this document, not from the source code.

## Registration

1. Username length is between 5 and 15 characters, inclusive.
2. Email contains a non-empty local part, `@`, and a domain with a dot.
3. Age is an integer between 18 and 60, inclusive.
4. Password length is between 8 and 20 characters, inclusive.
5. Password and confirmation are exactly equal.

Registration is accepted only when all five rules pass.

## Shipping and discount

1. Order value must be greater than 0 VND.
2. A VIP customer receives 10% discount when order value is at least 1,000,000 VND.
3. A valid coupon gives 5% discount when order value is at least 500,000 VND.
4. If both discounts qualify, only the higher discount is applied.
5. Local shipping costs 30,000 VND but is free from 800,000 VND. Remote shipping always costs 50,000 VND.

Final amount = order value − discount amount + shipping fee.

## Loan eligibility

1. Age is an integer between 21 and 60, inclusive.
2. Monthly income is at least 15,000,000 VND.
3. Credit score is an integer between 650 and 850, inclusive.
4. Employment status is `employed`.
5. Requested loan is positive and no more than 10 times monthly income.

The application is approved only when all five conditions pass.
