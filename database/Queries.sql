SELECT * FROM product;

SELECT count(pro_id) from product;

SELECT * From product Where pro_cat='Movie';

SELECT DISTINCT(pro_cat) FROM product;

SELECT sum(pro_price) FROM product;

Select sum(pro_price) FROM product Where pro_cat = 'Movie';

Drop Table product;