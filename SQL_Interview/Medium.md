Below are common SQL interview questions organized by topic. Each question includes small **example tables**, a **solution query**, and a short **explanation**. (SQL shown in ANSI/Postgres style.)

---

# Topic 1 — Joins

## Q1. List customers who have placed at least one order (inner join)

**Example tables**

**Customers**

| CustomerID | Name  | Email                                     |
| ---------: | ----- | ----------------------------------------- |
|          1 | Alice | [alice@acme.com](mailto:alice@acme.com)   |
|          2 | Bob   | [bob@example.org](mailto:bob@example.org) |
|          3 | Chris | [chris@foo.io](mailto:chris@foo.io)       |

**Orders**

| OrderID | CustomerID | OrderDate  |
| ------: | ---------: | ---------- |
|     101 |          1 | 2025-08-01 |
|     102 |          2 | 2025-08-03 |
|     103 |          1 | 2025-08-05 |

**Solution**

```sql
SELECT c.CustomerID, c.Name, o.OrderID, o.OrderDate
FROM Customers c
JOIN Orders o ON o.CustomerID = c.CustomerID;
```

**Explanation**
Inner join returns only customers with matching orders.

---

## Q2. List all customers and their order counts, including customers with zero orders (left join)

**Example tables** — use *Customers* and *Orders* from Q1 (note customer 3 has no orders)

**Solution**

```sql
SELECT c.CustomerID, c.Name, COUNT(o.OrderID) AS order_count
FROM Customers c
LEFT JOIN Orders o ON o.CustomerID = c.CustomerID
GROUP BY c.CustomerID, c.Name
ORDER BY c.CustomerID;
```

**Explanation**
Left join keeps all customers; `COUNT(o.OrderID)` counts only matched orders.

---

## Q3. Total spend per customer (join Orders→OrderItems)

**Example tables**

**OrderItems**

| OrderID | ProductID | Qty | UnitPrice |
| ------: | --------: | --: | --------: |
|     101 |        10 |   2 |     10.00 |
|     101 |        11 |   1 |     25.00 |
|     102 |        11 |   3 |     25.00 |
|     103 |        10 |   1 |     10.00 |

**Solution**

```sql
SELECT c.CustomerID, c.Name, SUM(oi.Qty * oi.UnitPrice) AS total_spend
FROM Customers c
JOIN Orders o     ON o.CustomerID = c.CustomerID
JOIN OrderItems oi ON oi.OrderID   = o.OrderID
GROUP BY c.CustomerID, c.Name
ORDER BY total_spend DESC;
```

**Explanation**
Join across tables and aggregate line totals.

---

## Q4. Self-join: list employees and their managers

**Example tables**

**Employees**

| EmpID | Name   | ManagerID |
| ----: | ------ | --------: |
|     1 | Dana   |      NULL |
|     2 | Ellen  |         1 |
|     3 | Faisal |         1 |

**Solution**

```sql
SELECT e.EmpID, e.Name AS employee, m.Name AS manager
FROM Employees e
LEFT JOIN Employees m ON m.EmpID = e.ManagerID
ORDER BY e.EmpID;
```

**Explanation**
Join the table to itself; top-level manager has NULL manager.

---

# Topic 2 — Aggregation & GROUP BY & HAVING

## Q1. Orders per day

**Example tables** — use *Orders* from Topic 1

**Solution**

```sql
SELECT OrderDate, COUNT(*) AS num_orders
FROM Orders
GROUP BY OrderDate
ORDER BY OrderDate;
```

**Explanation**
Group rows by date and count.

---

## Q2. Customers with more than 1 order (HAVING)

**Example tables** — *Customers*, *Orders*

**Solution**

```sql
SELECT c.CustomerID, c.Name, COUNT(o.OrderID) AS order_count
FROM Customers c
JOIN Orders o ON o.CustomerID = c.CustomerID
GROUP BY c.CustomerID, c.Name
HAVING COUNT(o.OrderID) > 1;
```

**Explanation**
`HAVING` filters after grouping.

---

## Q3. Average order value per customer

**Example tables** — *Orders*, *OrderItems*, *Customers*

**Solution**

```sql
WITH order_values AS (
  SELECT o.OrderID, o.CustomerID,
         SUM(oi.Qty * oi.UnitPrice) AS order_value
  FROM Orders o
  JOIN OrderItems oi ON oi.OrderID = o.OrderID
  GROUP BY o.OrderID, o.CustomerID
)
SELECT c.CustomerID, c.Name, AVG(order_value) AS avg_order_value
FROM order_values ov
JOIN Customers c ON c.CustomerID = ov.CustomerID
GROUP BY c.CustomerID, c.Name
ORDER BY avg_order_value DESC;
```

**Explanation**
First compute each order’s value, then average per customer.

---

## Q4. Top product by total revenue

**Example tables**

**Products**

| ProductID | ProductName    |
| --------: | -------------- |
|        10 | USB-C Cable    |
|        11 | Wireless Mouse |

**OrderItems** — from Topic 1 Q3

**Solution**

```sql
SELECT p.ProductID, p.ProductName,
       SUM(oi.Qty * oi.UnitPrice) AS revenue
FROM OrderItems oi
JOIN Products p ON p.ProductID = oi.ProductID
GROUP BY p.ProductID, p.ProductName
ORDER BY revenue DESC
FETCH FIRST 1 ROW ONLY; -- or LIMIT 1
```

**Explanation**
Aggregate revenue by product and pick the highest.

---

# Topic 3 — Window Functions

## Q1. Latest order per customer (ROW\_NUMBER)

**Example tables** — *Customers*, *Orders*

**Solution**

```sql
WITH ranked AS (
  SELECT o.*, ROW_NUMBER() OVER (
           PARTITION BY o.CustomerID ORDER BY o.OrderDate DESC
         ) AS rn
  FROM Orders o
)
SELECT OrderID, CustomerID, OrderDate
FROM ranked
WHERE rn = 1;
```

**Explanation**
Rank orders per customer by date and keep the most recent.

---

## Q2. Running total of daily sales

**Example tables** — *Orders*, *OrderItems*

**Solution**

```sql
WITH daily AS (
  SELECT o.OrderDate,
         SUM(oi.Qty * oi.UnitPrice) AS sales
  FROM Orders o
  JOIN OrderItems oi ON oi.OrderID = o.OrderID
  GROUP BY o.OrderDate
)
SELECT OrderDate,
       sales,
       SUM(sales) OVER (ORDER BY OrderDate
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM daily
ORDER BY OrderDate;
```

**Explanation**
Window `SUM` accumulates totals across ordered dates.

---

## Q3. Percent rank of orders by value

**Example tables** — *Orders*, *OrderItems*

**Solution**

```sql
WITH order_values AS (
  SELECT o.OrderID, SUM(oi.Qty * oi.UnitPrice) AS order_value
  FROM Orders o
  JOIN OrderItems oi ON oi.OrderID = o.OrderID
  GROUP BY o.OrderID
)
SELECT OrderID, order_value,
       PERCENT_RANK() OVER (ORDER BY order_value) AS pct_rank
FROM order_values
ORDER BY order_value;
```

**Explanation**
Window function gives relative position (0..1) in sorted list.

---

## Q4. 3-day moving average of sales

**Example tables** — daily sales derived as in Q2

**Solution**

```sql
WITH daily AS (
  SELECT o.OrderDate,
         SUM(oi.Qty * oi.UnitPrice) AS sales
  FROM Orders o
  JOIN OrderItems oi ON oi.OrderID = o.OrderID
  GROUP BY o.OrderDate
)
SELECT OrderDate, sales,
       AVG(sales) OVER (
         ORDER BY OrderDate
         ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS mov_avg_3
FROM daily
ORDER BY OrderDate;
```

**Explanation**
Moving window of the current and previous 2 days.

---

# Topic 4 — Subqueries & EXISTS

## Q1. Customers who ordered the product “Wireless Mouse” (IN)

**Example tables** — *Customers*, *Orders*, *OrderItems*, *Products*

**Solution**

```sql
SELECT DISTINCT c.CustomerID, c.Name
FROM Customers c
JOIN Orders o ON o.CustomerID = c.CustomerID
WHERE o.OrderID IN (
  SELECT oi.OrderID
  FROM OrderItems oi
  JOIN Products p ON p.ProductID = oi.ProductID
  WHERE p.ProductName = 'Wireless Mouse'
);
```

**Explanation**
Subquery finds order IDs containing the target product.

---

## Q2. Customers who never placed an order (NOT EXISTS)

**Example tables** — *Customers*, *Orders*

**Solution**

```sql
SELECT c.CustomerID, c.Name
FROM Customers c
WHERE NOT EXISTS (
  SELECT 1 FROM Orders o WHERE o.CustomerID = c.CustomerID
);
```

**Explanation**
`NOT EXISTS` returns customers with no matching rows in Orders.

---

## Q3. Orders whose value is above that customer’s average order value (correlated)

**Example tables** — *Orders*, *OrderItems*

**Solution**

```sql
WITH order_values AS (
  SELECT o.OrderID, o.CustomerID,
         SUM(oi.Qty * oi.UnitPrice) AS order_value
  FROM Orders o
  JOIN OrderItems oi ON oi.OrderID = o.OrderID
  GROUP BY o.OrderID, o.CustomerID
)
SELECT ov1.*
FROM order_values ov1
WHERE ov1.order_value > (
  SELECT AVG(ov2.order_value)
  FROM order_values ov2
  WHERE ov2.CustomerID = ov1.CustomerID
);
```

**Explanation**
Compare each order’s value to that customer’s own average.

---

## Q4. Products priced above their category average

**Example tables**

**Categories**

| CategoryID | CategoryName |
| ---------: | ------------ |
|          1 | Cables       |
|          2 | Mice         |

**Products**

| ProductID | ProductName    | CategoryID | Price |
| --------: | -------------- | ---------: | ----: |
|        10 | USB-C Cable    |          1 | 10.00 |
|        11 | Wireless Mouse |          2 | 25.00 |
|        12 | Gaming Mouse   |          2 | 40.00 |

**Solution**

```sql
SELECT p.*
FROM Products p
WHERE p.Price > (
  SELECT AVG(p2.Price)
  FROM Products p2
  WHERE p2.CategoryID = p.CategoryID
);
```

**Explanation**
Correlated subquery averages within each category.

---

# Topic 5 — Set Operations (UNION / INTERSECT / EXCEPT)

## Q1. Unique list of emails from Customers and MarketingEmails (UNION removes dups)

**Example tables**

**MarketingEmails**

| Email                                     |
| ----------------------------------------- |
| [alice@acme.com](mailto:alice@acme.com)   |
| [promo@brand.com](mailto:promo@brand.com) |

**Customers** — from earlier

**Solution**

```sql
SELECT Email FROM Customers
UNION
SELECT Email FROM MarketingEmails;
```

**Explanation**
`UNION` concatenates and de-duplicates.

---

## Q2. Emails that are both in Customers **and** MarketingEmails (INTERSECT)

**Example tables** — same as Q1

**Solution**

```sql
SELECT Email FROM Customers
INTERSECT
SELECT Email FROM MarketingEmails;
```

**Explanation**
`INTERSECT` keeps common rows.

---

## Q3. Customers who are **not** in the Marketing list (EXCEPT)

**Example tables** — same as Q1

**Solution**

```sql
SELECT Email FROM Customers
EXCEPT
SELECT Email FROM MarketingEmails;
```

**Explanation**
`EXCEPT` subtracts the second set from the first.

---

## Q4. Total rows when combining two result sets (UNION ALL)

**Example tables** — same as Q1

**Solution**

```sql
SELECT Email FROM Customers
UNION ALL
SELECT Email FROM MarketingEmails;
```

**Explanation**
`UNION ALL` keeps duplicates; useful for exact counts and faster than `UNION`.

---

# Topic 6 — String & Date Functions

## Q1. Extract email domain

**Example tables** — *Customers*

**Solution** (Postgres-style)

```sql
SELECT Email,
       SUBSTRING(Email FROM POSITION('@' IN Email) + 1) AS domain
FROM Customers;
```

**Explanation**
Takes substring after the `@`.

---

## Q2. Year-month sales totals

**Example tables** — *Orders*, *OrderItems*

**Solution**

```sql
WITH order_values AS (
  SELECT o.OrderID, o.OrderDate,
         SUM(oi.Qty * oi.UnitPrice) AS order_value
  FROM Orders o
  JOIN OrderItems oi ON oi.OrderID = o.OrderID
  GROUP BY o.OrderID, o.OrderDate
)
SELECT EXTRACT(YEAR  FROM OrderDate) AS yr,
       EXTRACT(MONTH FROM OrderDate) AS mon,
       SUM(order_value) AS sales
FROM order_values
GROUP BY EXTRACT(YEAR  FROM OrderDate), EXTRACT(MONTH FROM OrderDate)
ORDER BY yr, mon;
```

**Explanation**
Group by year/month extracted from the date.

---

## Q3. Orders placed on weekends

**Example tables** — *Orders*

**Solution** (Postgres: `EXTRACT(DOW)` Sunday=0)

```sql
SELECT *
FROM Orders
WHERE EXTRACT(DOW FROM OrderDate) IN (0, 6);
```

**Explanation**
Filter by day-of-week for Saturday/Sunday.

---

## Q4. Split full name to first and last (simple space split)

**Example tables**

**People**

| FullName        |
| --------------- |
| "Alice Johnson" |
| "Bob Lee"       |

**Solution** (Postgres-style)

```sql
SELECT FullName,
       SPLIT_PART(FullName, ' ', 1) AS FirstName,
       SPLIT_PART(FullName, ' ', 2) AS LastName
FROM People;
```

**Explanation**
Simple split by the first space (note: names can be more complex in real life).

---

## Bonus: Indexing quick tip

* Use an index on the **join keys** (`Orders.CustomerID`, `OrderItems.OrderID`) and on common **filtering columns** (e.g., `Orders.OrderDate`).
* Always `EXPLAIN` your query to verify index usage.
