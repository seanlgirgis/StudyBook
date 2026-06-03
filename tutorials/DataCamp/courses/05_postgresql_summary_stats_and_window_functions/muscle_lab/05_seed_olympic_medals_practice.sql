-- 05_seed_olympic_medals_practice.sql
-- Seeds olympic-style medals practice data (432 rows).

INSERT INTO course05_muscle.olympic_medals_practice (
    medal_id, year, city, sport, discipline, athlete, country, gender, event, medal
)
SELECT
    gs AS medal_id,
    (ARRAY[2000,2004,2008,2012,2016,2020])[((gs - 1) % 6) + 1] AS year,
    (ARRAY['Sydney','Athens','Beijing','London','Rio','Tokyo'])[((gs - 1) % 6) + 1] AS city,
    CASE ((gs - 1) % 8)
      WHEN 0 THEN 'Athletics'
      WHEN 1 THEN 'Athletics'
      WHEN 2 THEN 'Athletics'
      WHEN 3 THEN 'Athletics'
      WHEN 4 THEN 'Athletics'
      WHEN 5 THEN 'Weightlifting'
      WHEN 6 THEN 'Gymnastics'
      ELSE 'Swimming'
    END AS sport,
    CASE ((gs - 1) % 8)
      WHEN 0 THEN 'Athletics'
      WHEN 1 THEN 'Athletics'
      WHEN 2 THEN 'Athletics'
      WHEN 3 THEN 'Athletics'
      WHEN 4 THEN 'Athletics'
      WHEN 5 THEN 'Weightlifting'
      WHEN 6 THEN 'Gymnastics'
      ELSE 'Swimming'
    END AS discipline,
    (ARRAY['Noah Grant','Liam Carter','Mason Blake','Ethan Cole','Ava Reed','Mia Stone','Luna Hayes','Sora Kim','Yuna Park','Rin Sato','Leo Ivanov','Kai Petrov'])[((gs - 1) % 12) + 1] AS athlete,
    (ARRAY['USA','RUS','CHN','JPN','KOR','FRA','GBR','GER','DEN','NOR','SWE'])[((gs - 1) % 11) + 1] AS country,
    (ARRAY['Men','Women'])[((gs - 1) % 2) + 1] AS gender,
    (ARRAY['100M','10000M','Pole Vault','Discus Throw','Javelin Throw','69KG','Gymnastics Team','Swimming 100M Freestyle'])[((gs - 1) % 8) + 1] AS event,
    (ARRAY['Gold','Silver','Bronze'])[((gs - 1) % 3) + 1] AS medal
FROM generate_series(1, 432) AS gs;
