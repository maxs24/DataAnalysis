declare @colnames as varchar(4000), @query as varchar(4000), @colnamesnull as varchar(4000);

/*«адаем список названий колонок в результате (с ограничением из-за слишко больших данных)*/
select @colnames = stuff((select top 100 ', ' + '[' + CAST(Positions.INTERNAL_ORG_ORIGINAL_RK AS varchar(10)) + ']' 
						from dbo.Positions 
						ORDER BY Positions.INTERNAL_ORG_ORIGINAL_RK
						for xml path ('')), 1, 1, '');

select @colnamesnull = stuff((select top 100 ', isnull(' + '[' + CAST(Positions.INTERNAL_ORG_ORIGINAL_RK AS varchar(10)) + '],0) AS ' + '[' + CAST(Positions.INTERNAL_ORG_ORIGINAL_RK AS varchar(10)) + ']'
						from dbo.Positions 
						ORDER BY Positions.INTERNAL_ORG_ORIGINAL_RK
						for xml path ('')), 1, 1, '')

set @query = '
select APPLICATION_DT, ' + @colnamesnull + '
from (
select APPLICATION_DT, INTERNAL_ORG_ORIGINAL_RK, LOAN_AMOUNT
from dbo.CSV_Export) AS Ex
PIVOT(SUM(LOAN_AMOUNT) FOR INTERNAL_ORG_ORIGINAL_RK IN(' + @colnames +')) AS pvt
ORDER BY APPLICATION_DT';

execute(@query);