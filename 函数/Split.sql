if  exists (select * from sys.objects where object_id = OBJECT_ID(N'[dbo].[Split]') and type in (N'FN', N'IF', N'TF', N'FS', N'FT'))
drop function [dbo].[Split]
go
  CREATE FUNCTION[dbo].[Split](@Text VARCHAR(max),@Sign NVARCHAR(4000))  
 
RETURNS @tempTable TABLE(id INT IDENTITY(1,1)PRIMARY KEY,[VALUE]NVARCHAR(4000))  
 
AS  
 
BEGIN  --  select [dbo].[Split]('1,2',',')
 
DECLARE @StartIndex INT--开始查找的位置  
 
DECLARE @FindIndex INT--找到的位置  
 
DECLARE @Content VARCHAR(4000)--找到的值  
 
--初始化一些变量  
 
SET @StartIndex=1--T-SQL中字符串的查找位置是从1开始的  
 
SET @FindIndex=0 
 
--开始循环查找字符串逗号  
 
WHILE(@StartIndex<=LEN(@Text))  
 
BEGIN  
 
--查找字符串函数CHARINDEX第一个参数是要找的字符串  
 
--第二个参数是在哪里查找这个字符串  
 
--第三个参数是开始查找的位置  
 
--返回值是找到字符串的位置  
 
SELECT @FindIndex=CHARINDEX(@Sign,@Text,@StartIndex)  
 
--判断有没找到没找到返回0  
 
IF(@FindIndex=0 OR @FindIndex IS NULL)  
 
BEGIN  
 
--如果没有找到者表示找完了  
 
SET @FindIndex=LEN(@Text)+1  
 
END  
 
--截取字符串函数SUBSTRING第一个参数是要截取的字符串  
 
--第二个参数是开始的位置  
 
--第三个参数是截取的长度  
 
--@FindIndex-@StartIndex表示找的的位置-开始找的位置=要截取的长度  
 
--LTRIM和RTRIM是去除字符串左边和右边的空格函数  
 
SET @Content=LTRIM(RTRIM(SUBSTRING(@Text,@StartIndex,@FindIndex-@StartIndex)))  
 
--初始化下次查找的位置  
 
SET @StartIndex=@FindIndex+1  
 
--把找的的值插入到要返回的Table类型中  
 
INSERT INTO @tempTable([VALUE])VALUES(@Content)  
 
END  
 
RETURN  
 
END


go