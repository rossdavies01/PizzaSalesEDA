IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[pizza_ingredients]') AND type in (N'U'))
DROP TABLE [dbo].[pizza_ingredients]
GO


CREATE TABLE [dbo].[pizza_ingredients](
[ingredient_id] [int] IDENTITY(1,1) NOT NULL,
[ingredient] [varchar](50) NULL
) ON [PRIMARY]
GO


INSERT INTO [dbo].[pizza_ingredients]
SELECT DISTINCT(VALUE) AS ingredient
FROM [pizzasales_rpt]
CROSS APPLY STRING_SPLIT(pizza_ingredients,',')

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[order_pizza_ingredients]') AND type in (N'U'))
DROP TABLE [dbo].[order_pizza_ingredients]
GO

CREATE TABLE [dbo].[order_pizza_ingredients](
[order_id] [smallint] NULL,
[pizza_id] [bigint] NULL,
[ingredient_id] [int] NULL
) ON [PRIMARY]
GO

INSERT INTO [dbo].[order_pizza_ingredients]
SELECT [order_id],[pizza_id],(SELECT [ingredient_id] FROM [dbo].[pizza_ingredients] WHERE ingredient = VALUE)  AS ingredient_id
FROM [pizzasales_rpt] 
CROSS APPLY STRING_SPLIT(pizza_ingredients,',') 
ORDER BY order_id

SELECT 
*
FROM 
[dbo].[pizzasales_rpt] ps
JOIN [dbo].[order_pizza_ingredients] opi ON opi.order_id = ps.order_id and opi.pizza_id = ps.pizza_id
JOIN [dbo].[pizza_ingredients] pi ON pi.ingredient_id = opi.[ingredient_id]
WHERE ps.order_id = 1





