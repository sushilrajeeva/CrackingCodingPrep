Below is a curated set of **SQL interview questions** from **basic → advanced**. For each topic:

* Easy topics: **1–2** questions
* Harder/advanced topics: **3–4** questions

Each question includes **example tables (with sample rows)**, a **solution query**, and a brief **explanation**. SQL shown in ANSI/Postgres-like syntax.

---

# Topic 1 — SELECT & WHERE (Easy)

## Q1. Get all customers from New York City

**Example table — Customers**

| CustomerID | Name  | City        | State | Email                                   |
| ---------: | ----- | ----------- | ----- | --------------------------------------- |
|          1 | Alice | New York    | NY    | [alice@acme.com](mailto:alice@acme.com) |
|          2 | Bob   | Jersey City | NJ    | [bob@foo.com](mailto:bob@foo.com)       |
|          3 | Chris | New York    | NY    | [chris@bar.com](mailto:chris@bar.com)   |

**Solution**

```sql
SELECT CustomerID, Name, Email
FROM Customers
WHERE City = 'New York' AND State = 'NY';
```

**Explanation**: Basic filtering with `WHERE` and multiple predicates.

---

## Q2. Find products priced between \$10 and \$30

**Example table — Products**

| ProductID | ProductName    | Price |
| --------: | -------------- | ----: |
|        10 | USB-C Cable    | 10.00 |
|        11 | Wireless Mouse | 25.00 |
|        12 | Laptop Stand   | 35.00 |

**Solution**

```sql
SELECT *
FROM Products
WHERE Price BETWEEN 10 AND 30;
```

**Explanation**: `BETWEEN` is inclusive of both endpoints.

---

# Topic 2 — ORDER BY, LIMIT/OFFSET (Easy)

## Q1. Top 2 most expensive products

**Example table — Products** (same as above)

**Solution**

```sql
SELECT ProductID, ProductName, Price
FROM Products
ORDER BY Price DESC
FETCH FIRST 2 ROWS ONLY; -- or LIMIT 2
```

**Explanation**: Sort and trim the result set.

---

## Q2. Page 2 of customers ordered by name (page size 2)

**Example table — Customers** (same as above)

**Solution**

```sql
SELECT CustomerID, Name
FROM Customers
ORDER BY Name ASC
OFFSET 2 ROWS
FETCH NEXT 2 ROWS ONLY; -- or LIMIT 2 OFFSET 2
```

**Explanation**: Use `OFFSET`/`LIMIT` (or `FETCH`) for simple pagination.

---

# Topic 3 — Joins (Medium)

## Q1. List orders with customer name (INNER JOIN)

**Example tables**

**Orders**

| OrderID | CustomerID | OrderDate  |
| ------: | ---------: | ---------- |
|     101 |          1 | 2025-08-01 |
|     102 |          2 | 2025-08-02 |

**Customers** (from earlier)

**Solution**

```sql
SELECT o.OrderID, o.OrderDate, c.Name AS Customer
FROM Orders o
JOIN Customers c ON c.CustomerID = o.CustomerID;
```

**Explanation**: Return rows only when keys match.

---

## Q2. Customers and their order counts (LEFT JOIN)

**Example tables** — Customers, Orders

**Solution**

```sql
SELECT c.CustomerID, c.Name, COUNT(o.OrderID) AS order_count
FROM Customers c
LEFT JOIN Orders o ON o.CustomerID = c.CustomerID
GROUP BY c.CustomerID, c.Name
ORDER BY c.CustomerID;
```

**Explanation**: Keep all customers; unmatched orders contribute 0 to the count.

---

## Q3. Order line totals (JOIN Orders→OrderItems)

**Example table — OrderItems**

| OrderID | ProductID | Qty | UnitPrice |
| ------: | --------: | --: | --------: |
|     101 |        10 |   2 |     10.00 |
|     101 |        11 |   1 |     25.00 |
|     102 |        11 |   3 |     25.00 |

**Solution**

```sql
SELECT o.OrderID, o.OrderDate, SUM(oi.Qty * oi.UnitPrice) AS order_total
FROM Orders o
JOIN OrderItems oi ON oi.OrderID = o.OrderID
GROUP BY o.OrderID, o.OrderDate
ORDER BY o.OrderID;
```

**Explanation**: Join, compute line totals, and aggregate per order.

---

## Q4. Employee ↔ manager pairs (self-join)

**Example table — Employees**

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

**Explanation**: A table can join to itself to express hierarchies.

---

# Topic 4 — Aggregation, GROUP BY, HAVING (Medium)

## Q1. Orders per day

**Example table — Orders** (from earlier)

**Solution**

```sql
SELECT OrderDate, COUNT(*) AS num_orders
FROM Orders
GROUP BY OrderDate
ORDER BY OrderDate;
```

**Explanation**: Count rows by grouping column.

---

## Q2. Customers with more than 1 order (HAVING)

**Example tables** — Customers, Orders

**Solution**

```sql
SELECT c.CustomerID, c.Name, COUNT(o.OrderID) AS order_count
FROM Customers c
JOIN Orders o ON o.CustomerID = c.CustomerID
GROUP BY c.CustomerID, c.Name
HAVING COUNT(o.OrderID) > 1;
```

**Explanation**: `HAVING` filters groups after aggregation.

---

## Q3. Revenue per product

**Example tables** — OrderItems, Products

**Solution**

```sql
SELECT p.ProductID, p.ProductName, SUM(oi.Qty * oi.UnitPrice) AS revenue
FROM OrderItems oi
JOIN Products p ON p.ProductID = oi.ProductID
GROUP BY p.ProductID, p.ProductName
ORDER BY revenue DESC;
```

**Explanation**: Aggregate derived values by product.

---

## Q4. Average order value per customer

**Example tables** — Orders, OrderItems, Customers

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

**Explanation**: Compute per-order totals, then average per customer.

---

# Topic 5 — Subqueries (IN / EXISTS / Correlated) (Advanced)

## Q1. Customers who bought “Wireless Mouse” (IN)

**Example tables** — Customers, Orders, OrderItems, Products

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

**Explanation**: Subquery returns qualifying order IDs.

---

## Q2. Customers with no orders (NOT EXISTS)

**Example tables** — Customers, Orders

**Solution**

```sql
SELECT c.CustomerID, c.Name
FROM Customers c
WHERE NOT EXISTS (
  SELECT 1
  FROM Orders o
  WHERE o.CustomerID = c.CustomerID
);
```

**Explanation**: `NOT EXISTS` is efficient for anti-joins.

---

## Q3. Orders above that customer’s average (correlated)

**Example tables** — Orders, OrderItems

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

**Explanation**: Compare each order to its customer’s average via a correlated subquery.

---

## Q4. Products priced above their category average (correlated)

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

**Explanation**: Correlated subquery per category.

---

# Topic 6 — Set Operations (Easy/Medium)

## Q1. Unique emails from Customers and Marketing list (UNION)

**Example tables**

**MarketingEmails**

| Email                                     |
| ----------------------------------------- |
| [promo@brand.com](mailto:promo@brand.com) |
| [alice@acme.com](mailto:alice@acme.com)   |

**Customers** (has `Email` column from earlier)

**Solution**

```sql
SELECT Email FROM Customers
UNION
SELECT Email FROM MarketingEmails;
```

**Explanation**: `UNION` concatenates and removes duplicates.

---

## Q2. Emails present in both lists (INTERSECT)

**Example tables** — same as above

**Solution**

```sql
SELECT Email FROM Customers
INTERSECT
SELECT Email FROM MarketingEmails;
```

**Explanation**: Keeps only common rows.

---

# Topic 7 — Window Functions (Advanced)

## Q1. Latest order per customer (ROW\_NUMBER)

**Example tables** — Orders

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

**Explanation**: Rank within partitions and filter to `rn = 1`.

---

## Q2. Running total of daily sales

**Example tables** — Orders, OrderItems

**Solution**

```sql
WITH daily AS (
  SELECT o.OrderDate, SUM(oi.Qty * oi.UnitPrice) AS sales
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

**Explanation**: Cumulative window sum across ordered dates.

---

## Q3. Percent rank of orders by value

**Example tables** — Orders, OrderItems

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

**Explanation**: Relative position 0..1 among sorted values.

---

## Q4. 3-order moving average per customer

**Example tables** — Orders, OrderItems

**Solution**

```sql
WITH order_values AS (
  SELECT o.OrderID, o.CustomerID,
         SUM(oi.Qty * oi.UnitPrice) AS order_value,
         o.OrderDate
  FROM Orders o
  JOIN OrderItems oi ON oi.OrderID = o.OrderID
  GROUP BY o.OrderID, o.CustomerID, o.OrderDate
)
SELECT CustomerID, OrderID, OrderDate, order_value,
       AVG(order_value) OVER (
         PARTITION BY CustomerID
         ORDER BY OrderDate
         ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS mov_avg_3
FROM order_values
ORDER BY CustomerID, OrderDate;
```

**Explanation**: Moving window within each customer.

---

# Topic 8 — CTEs & Recursion (Advanced)

## Q1. Use a CTE to compute order totals, then filter

**Example tables** — Orders, OrderItems

**Solution**

```sql
WITH order_totals AS (
  SELECT o.OrderID, SUM(oi.Qty * oi.UnitPrice) AS total
  FROM Orders o
  JOIN OrderItems oi ON oi.OrderID = o.OrderID
  GROUP BY o.OrderID
)
SELECT *
FROM order_totals
WHERE total >= 50;
```

**Explanation**: CTE improves readability and reuse.

---

## Q2. Recursive CTE: employee hierarchy (manager chain)

**Example table — Employees** (from earlier)

**Solution**

```sql
WITH RECURSIVE hierarchy AS (
  SELECT EmpID, Name, ManagerID, 1 AS lvl
  FROM Employees
  WHERE ManagerID IS NULL
  UNION ALL
  SELECT e.EmpID, e.Name, e.ManagerID, h.lvl + 1
  FROM Employees e
  JOIN hierarchy h ON e.ManagerID = h.EmpID
)
SELECT * FROM hierarchy ORDER BY lvl, EmpID;
```

**Explanation**: Recursively walk parent→child relationships.

---

## Q3. Recursive CTE: running dates between two endpoints

**Example table — CalendarParams**

| StartDate  | EndDate    |
| ---------- | ---------- |
| 2025-08-01 | 2025-08-05 |

**Solution**

```sql
WITH RECURSIVE dates AS (
  SELECT StartDate AS d, EndDate
  FROM CalendarParams
  UNION ALL
  SELECT d + INTERVAL '1 day', EndDate
  FROM dates
  WHERE d < EndDate
)
SELECT d AS CalendarDate
FROM dates;
```

**Explanation**: Generate series via recursion.

---

# Topic 9 — Pivot / Unpivot (Medium/Advanced)

## Q1. Pivot: daily sales per product (static columns)

**Example tables** — Orders, OrderItems, Products

**Solution (illustrative)**

```sql
-- Build daily sales per product
WITH daily AS (
  SELECT o.OrderDate, p.ProductName, SUM(oi.Qty * oi.UnitPrice) AS sales
  FROM Orders o
  JOIN OrderItems oi ON oi.OrderID = o.OrderID
  JOIN Products p ON p.ProductID = oi.ProductID
  GROUP BY o.OrderDate, p.ProductName
)
SELECT OrderDate,
       SUM(CASE WHEN ProductName = 'USB-C Cable'    THEN sales END) AS usb_c_cable,
       SUM(CASE WHEN ProductName = 'Wireless Mouse' THEN sales END) AS wireless_mouse
FROM daily
GROUP BY OrderDate
ORDER BY OrderDate;
```

**Explanation**: Conditional aggregation emulates pivot.

---

## Q2. Unpivot: turn wide columns into rows

**Example table — SalesWide**

| OrderDate  | USB\_C\_Cable | Wireless\_Mouse |
| ---------- | ------------- | --------------- |
| 2025-08-01 | 20.00         | 25.00           |
| 2025-08-02 | 10.00         | 75.00           |

**Solution (generic approach)**

```sql
SELECT OrderDate, 'USB-C Cable' AS ProductName, USB_C_Cable AS Sales
FROM SalesWide
UNION ALL
SELECT OrderDate, 'Wireless Mouse', Wireless_Mouse
FROM SalesWide;
```

**Explanation**: Stack columns as rows; some DBs offer `UNPIVOT` syntax.

---

## Q3. Pivot: count orders by state

**Example tables** — Customers, Orders

**Solution**

```sql
WITH orders_per_state AS (
  SELECT c.State, COUNT(o.OrderID) AS cnt
  FROM Customers c
  LEFT JOIN Orders o ON o.CustomerID = c.CustomerID
  GROUP BY c.State
)
SELECT
  SUM(CASE WHEN State = 'NY' THEN cnt ELSE 0 END) AS ny_orders,
  SUM(CASE WHEN State = 'NJ' THEN cnt ELSE 0 END) AS nj_orders
FROM orders_per_state;
```

**Explanation**: Conditional sums convert categories to columns.

---

# Topic 10 — NULLs, CASE, COALESCE (Easy/Medium)

## Q1. Replace missing phone numbers with a placeholder

**Example table — Customers** (add Phone)

| CustomerID | Name  | Phone    |
| ---------: | ----- | -------- |
|          1 | Alice | 555-1010 |
|          2 | Bob   | NULL     |

**Solution**

```sql
SELECT CustomerID, Name, COALESCE(Phone, 'N/A') AS Phone
FROM Customers;
```

**Explanation**: `COALESCE` returns the first non-NULL value.

---

## Q2. Segment customers by spend bucket (CASE)

**Example tables** — Orders, OrderItems, Customers

**Solution**

```sql
WITH spend AS (
  SELECT c.CustomerID, c.Name, SUM(oi.Qty * oi.UnitPrice) AS total
  FROM Customers c
  JOIN Orders o ON o.CustomerID = c.CustomerID
  JOIN OrderItems oi ON oi.OrderID = o.OrderID
  GROUP BY c.CustomerID, c.Name
)
SELECT CustomerID, Name,
       CASE
         WHEN total >= 100 THEN 'Gold'
         WHEN total >= 50  THEN 'Silver'
         ELSE 'Bronze'
       END AS tier
FROM spend
ORDER BY total DESC;
```

**Explanation**: `CASE` maps numeric ranges to labels.

---

# Topic 11 — DML with Joins (Medium)

## Q1. Update product prices by a category-wide 10% increase

**Example tables** — Products, Categories

**Solution** (Postgres-style)

```sql
UPDATE Products p
SET Price = p.Price * 1.10
FROM Categories c
WHERE p.CategoryID = c.CategoryID
  AND c.CategoryName = 'Mice';
```

**Explanation**: `UPDATE … FROM` allows join-based updates.

---

## Q2. Delete customers who have no orders

**Example tables** — Customers, Orders

**Solution** (Postgres-style)

```sql
DELETE FROM Customers c
WHERE NOT EXISTS (
  SELECT 1 FROM Orders o WHERE o.CustomerID = c.CustomerID
);
```

**Explanation**: Anti-join deletion using `NOT EXISTS`.

---

## Q3. Insert top 1 daily product by revenue into a summary table

**Example tables** — Orders, OrderItems, Products; **SummaryTopProduct** target

| Day | ProductID | Revenue |
| --- | --------- | ------- |

**Solution**

```sql
WITH daily AS (
  SELECT o.OrderDate::date AS day, oi.ProductID,
         SUM(oi.Qty * oi.UnitPrice) AS revenue
  FROM Orders o
  JOIN OrderItems oi ON oi.OrderID = o.OrderID
  GROUP BY o.OrderDate::date, oi.ProductID
), ranked AS (
  SELECT day, ProductID, revenue,
         ROW_NUMBER() OVER (PARTITION BY day ORDER BY revenue DESC) AS rn
  FROM daily
)
INSERT INTO SummaryTopProduct (Day, ProductID, Revenue)
SELECT day, ProductID, revenue
FROM ranked
WHERE rn = 1;
```

**Explanation**: Use CTE + window ranking, then insert winners.

---

# Topic 12 — Indexes & Query Performance (Advanced)

> Note: Syntax for index creation varies slightly across DBs.

## Q1. Speed up lookups on Orders by CustomerID + OrderDate

**Example table — Orders**

**Solution**

```sql
CREATE INDEX idx_orders_customer_date
  ON Orders (CustomerID, OrderDate);

-- Query that benefits
SELECT *
FROM Orders
WHERE CustomerID = 1 AND OrderDate >= DATE '2025-08-01';
```

**Explanation**: Composite index supports equality on first column and range on second.

---

## Q2. Covering index for frequent product filter + projection

**Example table — Products**

**Solution**

```sql
-- Some DBs support INCLUDE columns (SQL Server, Postgres v11+ with INCLUDE)
CREATE INDEX idx_products_category_price
  ON Products (CategoryID, Price);

SELECT ProductID, ProductName, Price
FROM Products
WHERE CategoryID = 2 AND Price < 30;
```

**Explanation**: Index on filter columns reduces I/O; if index covers selected columns, fewer table lookups.

---

## Q3. Detect missing/unused indexes with EXPLAIN (concept)

**Example tables** — any

**Solution (pattern)**

```sql
EXPLAIN ANALYZE
SELECT o.OrderID
FROM Orders o
JOIN OrderItems oi ON oi.OrderID = o.OrderID
WHERE o.CustomerID = 1;
```

**Explanation**: `EXPLAIN` shows if scans use indexes (seek) or fall back to full scans; add indexes accordingly.

---

# Topic 13 — Transactions & Isolation (Advanced)

## Q1. Transfer funds atomically between two accounts

**Example table — Accounts**

| AccountID | CustomerID | Balance |
| --------: | ---------: | ------: |
|         1 |          1 |  200.00 |
|         2 |          1 |   50.00 |

**Solution**

```sql
BEGIN;
UPDATE Accounts SET Balance = Balance - 25.00 WHERE AccountID = 1;
UPDATE Accounts SET Balance = Balance + 25.00 WHERE AccountID = 2;
COMMIT; -- or ROLLBACK on error
```

**Explanation**: All statements succeed or none do, preserving consistency.

---

## Q2. Prevent dirty reads with READ COMMITTED

**Example tables** — Accounts

**Solution (concept)**

```sql
-- Session A
BEGIN;
UPDATE Accounts SET Balance = Balance - 25.00 WHERE AccountID = 1;
-- (not yet committed)

-- Session B
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT Balance FROM Accounts WHERE AccountID = 1; -- sees pre-transaction value
```

**Explanation**: READ COMMITTED blocks dirty reads of uncommitted changes.

---

## Q3. Avoid lost updates using SELECT … FOR UPDATE

**Example table — Accounts**

**Solution**

```sql
BEGIN;
SELECT Balance FROM Accounts WHERE AccountID = 1 FOR UPDATE;
-- do calculations client-side
UPDATE Accounts SET Balance = Balance - 10.00 WHERE AccountID = 1;
COMMIT;
```

**Explanation**: Row-level lock prevents concurrent writers from overwriting each other.

---

# Quick Study Tips

* Know when to use `INNER` vs `LEFT` joins.
* Prefer `EXISTS`/`NOT EXISTS` for semi/anti joins on large sets.
* Practice window functions (ranking, moving averages, partitions).
* Always verify performance with `EXPLAIN` and appropriate indexes.
