/*Топ 5 найпопулярніших статей*/
select title, count(title) as rating from links
    inner join article on links.link = article.article_id
                           group by title order by count(title) DESC limit 5;


/*Топ 5 статей з найбільшою кількістю посилань на інші статті*/
select title, count(title) as rating from links
    inner join article on links.parent = article.article_id
                           group by title order by count(title) DESC limit 5;


/*Топ 5 статей з найбільшою кількістю посилань на інші статті*/