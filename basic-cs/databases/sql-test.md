
# the original is from:
# https://www.bilibili.com/video/BV1Wg2cBtEex/?spm_id_from=333.788.top_right_bar_window_custom_collection.content.click&vd_source=e661a097b54f4d71d5e55b83834f00f2
# which seems to be professional and helpful for sql tests
# if you like it, you can support/star it



1. 23年蚂蚁-每个月Top3的周杰伦歌曲
原题链接：https://www.nowcoder.com/practice/4ab6d198ea8447fe9b6a1cad1f671503
SQL
select
`month`
,rk as ranking
,song_name
,cnt as play_pv
from
(
    select
    month(fdate) as `month`
    ,t1.song_id
    ,t3.song_name
    ,count(*) as cnt
    ,row_number()over(partition by month(fdate) order by count(*) desc, t1.song_id) as rk
    from play_log t1
    left join user_info t2
    on t1.user_id = t2.user_id
    left join song_info t3
    on t1.song_id = t3.song_id
    where t2.age between 18 and 25
    and year(fdate) = 2022
    and t3.singer_name = '周杰伦'
    group by month(fdate)
    ,t1.song_id
    ,t3.song_name
) tt
where rk <= 3
2. 23年蚂蚁-最长连续登录天数
原题链接：https://www.nowcoder.com/practice/cb8bc687046e4d32ad38de62c48ad79b?tpId=375&tags=&title=&difficulty=0&judgeStatus=0&rp=0&sourceUrl=%2Fexam%2Foj
SQL
select
user_id
,max(cnt) as max_consec_days
from
(
    select
    user_id
    ,tmp_dt
    ,count(1) as cnt
    from
    (
        select
        fdate
        ,user_id
        ,date_sub(fdate, interval rk day) as tmp_dt
        from
        (
            select
            *
            ,row_number()over(partition by user_id order by fdate) as rk
            from
            (
                select
                fdate
                ,user_id
                from tb_dau
                where fdate >= '2023-01-01'
                and fdate <= '2023-01-31'
                group by 1, 2
            ) t1
        ) t2
    ) t3
    group by 1, 2
) t4
group by 1
3. 23年蚂蚁-分析客户逾期情况
原题链接：https://www.nowcoder.com/practice/22633632da344e2492973ecf555e10c9?tpId=375&tags=&title=&difficulty=0&judgeStatus=0&rp=0&sourceUrl=%2Fexam%2Foj
SQL
with tmp
as(
    select
    customer_id
    ,max(case when overdue_days is not null then 1 else 0 end) as is_overdue
    from loan_tb
    group by customer_id
)

select
t1.pay_ability
,concat(round(sum(t2.is_overdue) / count(t1.customer_id) * 100, 1), '%') as overdue_ratio
from customer_tb t1
left join tmp t2
on t1.customer_id = t2.customer_id
group by 1
order by 2 desc
4. 23年蚂蚁-获取指定客户每月的消费额
原题链接：https://www.nowcoder.com/practice/ed04f148b63e469e8f62e051d06a46f5?tpId=375&tags=&title=&difficulty=0&judgeStatus=0&rp=0&sourceUrl=%2Fexam%2Foj
SQL
select
left(t_time, 7) as `time`
,sum(t_amount) as total
from trade
where t_cus = 101
and t_type = 1
and year(t_time) = 2023
group by 1
order by 1
5. 23年蚂蚁-查询连续入住多晚的客户信息？
原题链接：https://www.nowcoder.com/practice/5b4018c47dfd401d87a5afb5ebf35dfd
SQL
select
t1.user_id
,t1.room_id
,t2.room_type
,datediff(checkout_time, checkin_time) as days
from checkin_tb t1
left join guestroom_tb t2
on t1.room_id = t2.room_id
where left(t1.checkin_time, 10) = '2022-06-12'
and datediff(checkout_time, checkin_time) >= 2
order by 4, 2, 1 desc
6. 23年蚂蚁-统计所有课程参加培训人次
原题链接：https://www.nowcoder.com/practice/98aad5807cf34a3b960cc8a70ce03f53
SQL
select
count(course1) + count(course2) + count(course3) as staff_nums
from
(
    select
    staff_id
    ,case when course like '%1%' then 'course1' end as course1
    ,case when course like '%2%' then 'course2' end as course2
    ,case when course like '%3%' then 'course3' end as course3
    from cultivate_tb
) t1
7. 23年蚂蚁-查询培训指定课程的员工信息
原题链接：https://www.nowcoder.com/practice/a0ef4574056e4a219ee7d651ba82efef
SQL
select
t1.staff_id
,t2.staff_name
from
(
    select distinct
    staff_id
    from cultivate_tb
    where course like '%3%'
) t1
left join staff_tb t2
on t1.staff_id = t2.staff_id
8. 23年蚂蚁-推荐内容准确的用户平均评分
原题链接：https://www.nowcoder.com/practice/2dcac73b647247f0aef0b261ed76b47e
SQL
select
avg(score) as avg_score
from
(
    select
    user_id
    ,max(score) as score
    from user_action_tb t1
    left join recommend_tb t2
    on t1.user_id = t2.rec_user
    and t1.hobby_l = t2.rec_info_l
    where t2.rec_id is not null
    group by 1
) tt
9. 23年携程-每个商品的销售总额
原题链接：https://www.nowcoder.com/practice/6d796e885ee44a9cb599f47b16a02ea4
SQL
select
t1.name as product_name
,t2.quantity as total_sales
,row_number()over(partition by t1.category order by t2.quantity desc, t1.product_id) as category_rank
from products t1
left join 
(
    select
    product_id
    ,sum(quantity) as quantity
    from orders
    group by 1
) t2
on t1.product_id = t2.product_id
where t2.product_id is not null
order by t1.category, t2.quantity desc
10. 22年携程-统计各岗位员工平均工作时长
原题链接：https://www.nowcoder.com/practice/b7220791a95a4cd092801069aefa1cae
SQL
select
t2.post
,sum(timestampdiff(minute, t1.first_clockin, t1.last_clockin) / 60.0) / count(distinct t2.staff_id) as work_hours
from attendent_tb t1
left join staff_tb t2
on t1.staff_id = t2.staff_id
where first_clockin is not null
and last_clockin is not null
group by 1
order by 2 desc
11. 22年携程-查询连续登陆的用户
原题链接：https://www.nowcoder.com/practice/9944210610ec417e94140ac09512a3f5
SQL
select
user_id
from
(
    select
    *
    ,date_sub(dt, interval rk day) as tmp_dt
    from
    (
        select
        t1.user_id
        ,date(t1.log_time) as dt
        ,row_number()over(partition by t1.user_id order by date(t1.log_time)) as rk
        from login_tb t1
        left join register_tb t2
        on t1.user_id = t2.user_id
        where t2.user_id is not null
    ) t3
) t4
group by 1, tmp_dt
having count(1) >= 3
order by 1
12. 23年携程-统计商家不同会员每日访问人次及访问人数
原题链接：https://www.nowcoder.com/practice/0017dc22426b495889da3304dcf254d1
SQL
select
t2.vip
,count(1) as visit_nums
,count(distinct t1.user_id) as visit_users
from visit_tb t1
left join uservip_tb t2
on t1.user_id = t2.user_id
group by 1
order by 2 desc
13. 23年携程-统计各等级会员用户下订单总额
原题链接：https://www.nowcoder.com/practice/48dd35a3dd8c4e1494db36b097a03300
SQL
select
t1.vip
,coalesce(sum(t2.order_price), 0) as order_total
from uservip_tb t1
left join 
(
    select
    user_id
    ,sum(order_price) as order_price
    from order_tb
    group by 1
) t2
on t1.user_id = t2.user_id
group by 1
order by 2 desc
14. 23年携程-查询下订单用户访问次数？
原题链接：https://www.nowcoder.com/practice/32bc1e0fce2343ad934b76a025e09fc5
SQL
select
user_id
,count(1) as visit_nums
from visit_tb
where user_id in (
    select distinct
    user_id
    from order_tb
    where left(order_time, 10) = '2022-09-02'
)
and left(visit_time, 10) = '2022-09-02'
group by 1
order by 2 desc
15. 23年携程-统计用户从访问到下单的转化率
原题链接：https://www.nowcoder.com/practice/eaff8684aed74e208300f2737edbb083
SQL
select
t2.dt as `date`
,concat(round(t1.cnt / t2.cnt * 100, 1), '%') as cr
from  
(
    select
    substr(order_time, 1, 10) as dt
    ,count(distinct user_id) as cnt
    from order_tb
    group by 1
) t1
left join 
(
    select
    substr(visit_time, 1, 10) as dt
    ,count(distinct user_id) as cnt
    from visit_tb
    group by 1
) t2
on t1.dt = t2.dt
16. 23年携程-统计员工薪资扣除比例
原题链接：https://www.nowcoder.com/practice/08db6f0135664ca598b579f8d53dc486
SQL
select
t1.staff_id
,t2.staff_name
,concat(round(dock_salary / normal_salary * 100, 1), '%') as dock_ratio
from salary_tb t1
left join staff_tb t2
on t1.staff_id = t2.staff_id
where t2.department = 'dep1'
order by 3 desc
17. 24金银交科-统计用户获得积分
原题链接：https://www.nowcoder.com/practice/22ed0cd240824bb597b3130fef389cea
SQL
select
user_id
,sum(timestampdiff(minute, visit_time, leave_time) div 10) as point
from visit_tb
group by 1
order by 2 desc
18. 22年携程-更新用户积分信息
原题链接：https://www.nowcoder.com/practice/ef1f2fda4338460b948810f3f7e7a68e
SQL
select
t1.user_id
,t1.point + t2.point as point
from uservip_tb t1
left join
(
    select
    user_id
    ,sum(order_price) as point
    from order_tb
    where order_price > 100
    group by 1
) t2
on t1.user_id = t2.user_id
where t2.point is not null
order by 2 desc
19. 22年携程-查询单日多次下订单的用户信息
原题链接：https://www.nowcoder.com/practice/9958aed1e74a49b795dfe2cb9d54ee12
SQL
select
substr(t1.order_time, 1, 10) as order_date
,t1.user_id
,count(1) as order_nums
,max(t2.vip) as vip
from order_tb t1
left join uservip_tb t2
on t1.user_id = t2.user_id
group by 1, 2
having count(1) > 1
order by 3 desc
20. 22年携程-统计各个部门平均薪资
原题链接：https://www.nowcoder.com/practice/4722fdf89a4c43eebb58d61a19ccab31
SQL
select
t2.department
,round(avg(t1.normal_salary - t1.dock_salary), 3) as avg_salary
from salary_tb t1
left join staff_tb t2
on t1.staff_id = t2.staff_id
where t1.normal_salary - t1.dock_salary >= 4000
and t1.normal_salary - t1.dock_salary <= 30000
group by 1
order by 2 desc
21. 22年携程-统计加班员工占比
原题链接：https://www.nowcoder.com/practice/6c0a521c36e14c7599eaef858f6f8233
SQL
select
t2.department
,concat(round(sum(if(timestampdiff(minute, t1.first_clockin, t1.last_clockin) / 60 > 9.5, 1, 0)) / count(t1.staff_id) * 100, 1), '%') as ratio
from attendent_tb t1
left join staff_tb t2
on t1.staff_id = t2.staff_id
group by 1
order by 2 desc



select
t1.department
,concat(round(sum(is_later) / count(1) * 100, 1), '%') as ratio
from staff_tb t1
left join
(
    select
    staff_id
    ,if(timestampdiff(minute, first_clockin, last_clockin) / 60 > 9.5, 1, 0) as is_later
    from attendent_tb
) t2
on t1.staff_id = t2.staff_id
group by 1
order by 2 desc
22. 22年携程-每天登陆最早的用户的内容喜好
原题链接：https://www.nowcoder.com/practice/24bb13a28267486ba86c1d21459fa90a
SQL
select
substr(log_time, 1, 10) as log_day
,t1.user_id
,t2.hobby
from
(
    select
    *
    ,dense_rank()over(partition by substr(log_time, 1, 10) order by log_time) as rk
    from login_tb
) t1
left join user_action_tb t2
on t1.user_id = t2.user_id
where rk = 1
order by 1
23. 22年携程-支付间隔平均值
原题链接：https://www.nowcoder.com/practice/847431ad931e45348eb1ab5657144c28
SQL
select
cast(avg(abs(timestampdiff(second, t1.logtime, t2.logtime))) as signed) as gap
from order_log t1
left join select_log t2
on t1.order_id = t2.order_id
24. 22年网易-网易云音乐推荐(网易校招笔试真题)
原题链接：https://www.nowcoder.com/practice/048ed413ac0e4cf4a774b906fc87e0e7
SQL
select
t2.music_name
from
(
    select distinct
    music_id
    from music_likes
    where user_id in (
        select distinct
        follower_id
        from follow
        where user_id = 1
    )
    and music_id not in (
        select distinct
        music_id
        from music_likes
        where user_id = 1
    )
) t1
left join music t2
on t1.music_id = t2.id
order by t1.music_id
25. 22年网易-商品交易
原题链接：https://www.nowcoder.com/practice/f257dfc1b55e42e19eec004aa3cb4174
SQL
select
t1.*
,t2.cnt
from goods t1
left join
(
    select
    goods_id
    ,sum(count) as cnt
    from trans 
    group by 1
) t2
on t1.id = t2.goods_id
where t1.weight < 50 and t2.cnt > 20
order by 1
26. 23年知乎-粉丝ctr
原题链接：https://www.nowcoder.com/practice/853a6567cf524f63bab0879b8d0bfe62
Python
select sum(read_num) / sum(show_num) fans_ctr
from c 
join b 
on c.content_id = b.content_id
join a 
on a.author_id = b.author_id
and c.fans_id = a.fans_id

27. 23年掌阅-查询成绩
原题链接：https://www.nowcoder.com/practice/ef30689ae065434c89c129e9dfe1b4cd
SQL
select
count(*)
from
(
    select
    sid
    from SC
    group by sid
    having avg(score) > 60
) t1

28. 24年OPPO-被重复观看次数最多的3个视频
原题链接：https://www.nowcoder.com/practice/b75fa2412659422c96369976ee1f9504
SQL
select
*
from
(
    select
    t1.cid
    ,sum(t1.cnt) as cnt
    ,row_number()over(order by sum(t1.cnt) desc, max(t2.release_date) desc) as rk
    from
    (
        select
        uid
        ,cid
        ,count(1) as cnt
        from play_record_tb
        group by 1, 2 
        having count(1) >= 2
    ) t1
    left join course_info_tb t2
    on t1.cid = t2.cid
    group by 1
    order by 3
) t2
where rk <= 3

29. 24年OPPO-短视频直播间晚上11-12点之间各直播间的在线人数
原题链接：https://www.nowcoder.com/practice/38f5febc9dac4e9e84ed5891a3e4ca05
SQL
select
t1.room_id
,t2.room_name
,count(distinct t1.user_id) as user_count
from user_view_tb t1
left join room_info_tb t2 
on t1.room_id = t2.room_id
where t1.in_time <= '23:59:59' and t1.out_time >= '23:00:00'
group by t1.room_id, t2.room_name
order by 3 desc

30. 23年阿里-淘宝店铺的实际销售额与客单价
原题链接：https://www.nowcoder.com/practice/ce116419a1f141568094b5eab70e5ce8
SQL
select
sum(t1.sales_num * t2.goods_price) as sales_total
,sum(t1.sales_num * t2.goods_price) / count(distinct t1.user_id)
from sales_tb t1
left join goods_tb t2
on t1.goods_id = t2.goods_id
where left(t1.sales_date, 7) = '2021-12'
and right(t1.sales_date, 2) between 20 and 31

31. 23年阿里-完成员工考核试卷突出的非领导员工
原题链接：https://www.nowcoder.com/practice/422dcd6ae72c49c9bbec1aff90d69806
SQL
select
t1.emp_id
,t2.emp_level
,t3.tag
from
(
    select
    emp_id
    ,score
    ,exam_id
    ,timestampdiff(second, start_time, submit_time) as cost_time
    ,avg(score)over(partition by exam_id) as avg_score
    ,avg(timestampdiff(second, start_time, submit_time))over(partition by exam_id) as avg_cost_time
    from exam_record 
) t1
left join emp_info t2
on t1.emp_id = t2.emp_id
left join examination_info t3
on t1.exam_id = t3.exam_id
where t1.score > t1.avg_score
and t1.cost_time < t1.avg_cost_time
and t2.emp_level < 7
order by 1

32. 23年京东-查询产生理赔费用的快递信息
https://www.nowcoder.com/practice/d22eab8a0001443fba7c5757e7cbcaea
SQL
select
t1.exp_number
,t2.exp_type
,t1.claims_cost
from exp_cost_tb t1
left join express_tb t2
on t1.exp_number = t2.exp_number
where t1.claims_cost is not null
order by 3 desc

33. 23年京东-统计快递运输时长
https://www.nowcoder.com/practice/bb4196936f15424dbabe76a501186d91
SQL
select
t2.exp_type
,round(avg(timestampdiff(minute, t1.out_time, t1.in_time) / 60.0), 1) as `time`
from exp_action_tb t1
left join express_tb t2
on t1.exp_number = t2.exp_number
group by 1
order by 2

34. 23年京东-统计快递从创建订单到发出间隔时长
https://www.nowcoder.com/practice/be3e56c950724b27aa79b79309147443
SQL
select
round(avg(timestampdiff(minute, t2.create_time, t1.out_time) / 60.0), 3) as `time`
from exp_action_tb t1
left join express_tb t2
on t1.exp_number = t2.exp_number

35. 23年京东-下单最多的商品
https://www.nowcoder.com/practice/be3e56c950724b27aa79b79309147443
SQL
select
product_id
,count(1) as cnt
from user_client_log
where step = 'order' -- 下单的订单
group by 1
order by 2 desc, 1
limit 1

36. 23年京东-用户购买次数前三
https://www.nowcoder.com/practice/e359c071d29c4fb7bac6d346f0cfe1d0
SQL
select
uid
,count(1) cnt
from user_client_log
where step = 'order'
group by 1
order by 2 desc, 1
limit 3

37. 23年京东-商品价格排名
https://www.nowcoder.com/practice/119f5b8cfe5b45779a3e1b3f4d83b341
SQL
select
product_id
,product_name
,type
,price      
from
(
    select
    *
    ,dense_rank()over(partition by type order by price desc) as rk
    from product_info
) t1
where rk <= 2
order by 4 desc, 2
limit 3

38. 23年京东-商品销售排名        
傻逼题目
https://www.nowcoder.com/practice/79c6c3d6d66946f79387bca73c0a29f4
SQL
select
t2.product_name
,cast(sum(t2.price) as signed) as GMV
from user_client_log t1
left join product_info t2
on t1.product_id = t2.product_id
where t1.step = 'select'
group by 1
order by 2 desc
limit 2
39. 23年京东-商品销售总额分布
https://www.nowcoder.com/practice/62909494cecd4eab8c2501167e825566
SQL
select
case when pay_method = '' then 'error' else pay_method end as pay_method -- 神人题
,count(1) as cnt
from user_client_log
where product_id = 'p100'
and step = 'select'
group by 1
order by 2 desc
40. 24年京东-每个客户的账户总金额
https://www.nowcoder.com/practice/19f0bc2b8cad44b6986ad9a51ed43def
SQL
select
customer_id
,sum(balance) as sum_balance
from account
group by 1
order by 2 desc
41. 24年京东-每个部门薪资排名前两名员工        
https://www.nowcoder.com/practice/89329eadd4a64126b1cd326ea0b7eff7
SQL
select
department
,employee_name
,salary
from
(
    select
    *
    ,rank()over(partition by department order by salary desc) as rk 
    from employees
) t1
where rk <= 2
order by 1, 3 desc

42. 24年京东-查询订单       
https://www.nowcoder.com/practice/5ae7f48dc94f4a76b0ade40b70caf308
SQL
select
order_id
,customer_name
,order_date
from
(
    select
    t1.order_id
    ,t1.customer_id
    ,t2.customer_name
    ,t1.order_date
    ,row_number()over(partition by t1.customer_id order by order_date desc) as rk
    from orders t1
    left join customers t2
    on t1.customer_id = t2.customer_id
) t1
where rk = 1
order by 2

43. 24年京东-商品id数据清洗统计     
https://www.nowcoder.com/practice/c985ecbd820b46e6bafa858f6600126d
SQL
select
substring_index(order_id, '_', -1) as product_id
,count(1) as cnt
from order_log
group by 1
order by 1

44. 24年京东-每个顾客最近一次下单的订单信息        
https://www.nowcoder.com/practice/4762ea22b0eb42ceb4f0a972c56d24c4
SQL
select
order_id
,customer_name
,order_date
from
(
    select
    t1.*
    ,t2.customer_name
    ,row_number()over(partition by customer_id order by order_date desc) as rk
    from orders t1
    left join customers t2
    on t1.customer_id = t2.customer_id
) tt
where rk = 1

45. 24年阿里-统计每个产品的销售情况
https://www.nowcoder.com/practice/d431aa7bf72c4fd7b048ec639bc83ad2
SQL
select
t1.*
,t2.customer_age_group
from
(
    select
    product_id
    ,sum(amount) as total_sales
    ,max(unit_price) as unit_price
    ,sum(quantity) as total_quantity
    ,round(sum(amount) / 12, 2) as avg_monthly_sales
    ,max(quantity) as max_monthly_quantity
    from
    (
        select
        t2.product_id
        ,substr(t1.order_date, 1, 7) as mon
        ,sum(t1.quantity * t2.unit_price) as amount
        ,sum(t1.quantity) as quantity
        ,max(t2.unit_price) as unit_price
        from orders t1
        left join products t2
        on t1.product_id = t2.product_id
        where substr(t1.order_date, 1, 4) = '2023'
        group by 1, 2
    ) t1
    group by 1
) t1 -- 产品id
left join 
(
    select
    *
    ,row_number()over(partition by product_id order by quantity desc, customer_age_group) as rk
    from
    (
        select
        t1.product_id
        ,case WHEN t2.customer_age BETWEEN 1 AND 10 THEN '1-10'
            WHEN t2.customer_age BETWEEN 11 AND 20 THEN '11-20'
            WHEN t2.customer_age BETWEEN 21 AND 30 THEN '21-30'
            WHEN t2.customer_age BETWEEN 31 AND 40 THEN '31-40'
            WHEN t2.customer_age BETWEEN 41 AND 50 THEN '41-50'
            WHEN t2.customer_age BETWEEN 51 AND 60 THEN '51-60'
            WHEN t2.customer_age >= 61 THEN '61+'
        ELSE '未知' 
        end as customer_age_group
        ,sum(t1.quantity) as quantity
        from orders t1
        left join customers t2
        on t1.customer_id = t2.customer_id
        group by 1, 2
    ) tt
) t2
on t1.product_id = t2.product_id
and rk = 1
order by 2 desc, 1

46. 24年京东-各个部门实际平均薪资和男女员工实际平均薪资
https://www.nowcoder.com/practice/e8272685d07347cc88667f31f7989231
SQL
select
t2.department
,round(avg(t1.normal_salary - t1.dock_salary), 2) as average_actual_salary
,coalesce(round(sum(case when t2.staff_gender = 'male' then t1.normal_salary - t1.dock_salary else 0 end) / count(distinct case when t2.staff_gender = 'male' then t1.staff_id else null end), 2), 0.00) as average_actual_salary_male
,coalesce(round(sum(case when t2.staff_gender = 'female' then t1.normal_salary - t1.dock_salary else 0 end) / count(distinct case when t2.staff_gender = 'female' then t1.staff_id else null end), 2), 0.00) as average_actual_salary_female
from salary_tb t1
left join staff_tb t2
on t1.staff_id = t2.staff_id
group by 1
order by 2 desc

47. 24年京东-每个顾客购买的最新产品名称        
https://www.nowcoder.com/practice/6ff37adae90f490aafa313033a2dcff7
SQL
select
t1.customer_id
,t2.customer_name
,t3.product_name as latest_order
from
(
    select
    *
    ,row_number()over(partition by customer_id order by order_date desc) as rk
    from orders
) t1
left join customers t2
on t1.customer_id = t2.customer_id
left join products t3
on t1.product_id = t3.product_id
where rk = 1
order by 1

48. 24年京东-输出播放量最高的视频 
https://www.nowcoder.com/practice/9e9cb264e1f64e28846975d5a32ba8e4
SQL
with tmp
as(
    select
    uid
    ,cid
    ,start_time as `time`
    ,1 as state
    from play_record_tb

    union all

    select
    uid
    ,cid
    ,end_time as `time`
    ,-1 as state
    from play_record_tb
)

select
cid
,max(uv) as max_peak_uv
from
(
    select
    uid
    ,cid
    ,sum(state)over(partition by cid order by `time`) as uv
    from tmp
) t1
group by 1
order by 2 desc
limit 3

49. 24年京东-返回顾客名称和相关订单号以及每个订单的总价
https://www.nowcoder.com/practice/4dda66e385c443d8a11570a70807d250
SQL
select
t2.cust_name
,t1.order_num
,t3.quantity * t3.item_price as OrderTotal
from Orders t1
left join Customers t2
on t1.cust_id = t2.cust_id
left join OrderItems t3
on t1.order_num = t3.order_num
order by 1, 2

50. 24年京东-未下单用户统计
https://www.nowcoder.com/practice/3433aee5c7824255b2dd2879b30df090
SQL
select 
count(distinct uid) as cnt
from user_info
where uid not in (
    select
    uid
    from order_log
)

51. 24年京东-用户订单信息查询
 https://www.nowcoder.com/practice/dccec8456d774169925c0d50843ea076
SQL
select
t2.city
,sum(total_amount) as total_order_amount
from orders t1
left join customers t2
on t1.customer_id = t2.customer_id
group by 1
order by 2 desc, 1

52. 24年京东-未下单用户登陆渠道统计
https://www.nowcoder.com/practice/5090553d7854458987997a5c91c30975
SQL
select
channel
,count(1) as cnt
from user_info
where uid not in (
    select distinct
    uid
    from order_log
)
group by 1
order by 2 desc, 1
limit 1

53. 24年京东-更新员工信息表
https://www.nowcoder.com/practice/1eb20d4bf7c5443da7b84105372c9070
SQL
select
t1.EMPLOYEE_ID
,case when t1.LAST_UPDATE_DT >= t2.UPDATE_DT then t1.POSITION else t2.NEW_POSITION end as POSITION
,case when t1.LAST_UPDATE_DT >= t2.UPDATE_DT then t1.LAST_UPDATE_DT else t2.UPDATE_DT end as LAST_UPDATE_DT
from EMPLOYEE_INFO t1
left join 
(
    select
    *
    ,row_number()over(partition by EMPLOYEE_ID order by UPDATE_DT desc) as rk
    from EMPLOYEE_UPDATE
) t2
on t1.EMPLOYEE_ID = t2.EMPLOYEE_ID 
and t2.rk = 1
order by 1

54. 24年京东-最受欢迎的top3课程
 https://www.nowcoder.com/practice/b9b33659559c46099aa3257da0374a48
SQL
select
t1.cid 
,count(1) as pv
,sum(timestampdiff(minute, t1.start_time, t1.end_time)) as time_len
from play_record_tb t1
left join course_info_tb t2
on t1.cid = t2.cid
where datediff(t1.start_time, date(t2.release_date)) <= 6
group by 1
having avg(score) >= 3
order by 2 desc, 3 desc
limit 3

55. 24年京东-对商品的销售情况进行深度分析
https://www.nowcoder.com/practice/d6ced1b60af64a4998169ae717672e8e
SQL
select
t2.category as product_category
,t3.age_group
,sum(t1.price * t1.quantity) as total_sales_amount
,round(sum(t1.price * t1.quantity) / sum(sum(t1.price * t1.quantity))over(partition by t2.category), 2) as purchase_percentage
from sales t1
left join products t2
on t1.product_id = t2.product_id
left join customer_info t3
on t1.sale_id = t3.sale_id
group by 1, 2
order by 1, 4 desc

56. 24年京东-电商平台需要对商家的销售业绩、退款情况和客户满意度进行综合评估
https://www.nowcoder.com/practice/48a236567617449eb6010274b30b29e8
SQL
-- merchants_underline 商家名称、行业
-- sales_underline 商家销售额
-- refunds_underline 商家退款额
-- satisfaction_underline 商家满意度
-- 查每个商家：名称、销售额、退款额、平均满意度

select
t1.merchant_id 
,t1.merchant_name 
,t2.total_sales_amount
,t3.total_refund_amount
,round(t4.average_satisfaction_score, 2) as average_satisfaction_score
from merchants_underline t1
left join 
(
    select
    merchant_id
    ,sum(sale_amount) as total_sales_amount
    from sales_underline
    group by 1
) t2
on t1.merchant_id = t2.merchant_id
left join 
(
    select
    merchant_id
    ,sum(refund_amount) as total_refund_amount
    from refunds_underline
    group by 1
) t3
on t1.merchant_id = t3.merchant_id
left join 
(
    select
    merchant_id
    ,avg(satisfaction_score) as average_satisfaction_score
    from satisfaction_underline
    group by 1
) t4
on t1.merchant_id = t4.merchant_id
order by 1

57. 24年京东-电商平台想要了解不同商品在不同月份的销售趋势
https://www.nowcoder.com/practice/a3fab87aca9347c28f406088cf601c7b
SQL
select
t1.product_id
,t2.product_name
,sum(t1.quantity) as total_sales
,max(t1.quantity) as max_monthly_sales
,min(t1.quantity) as min_monthly_sales
,cast(avg(t1.quantity) as signed) as avg_monthly_sales
from sales_underline t1
left join products_underline t2
on t1.product_id = t2.product_id
where sale_month in ('2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06')
group by 1, 2
order by 1

58. 24年京东-分析每个商品在不同时间段的销售情况
https://www.nowcoder.com/practice/eec7a93e1ab24233bd244e04e910d2f9
SQL
select
product_id
,product_name
,q2_2024_sales_total
,category_rank
,supplier_name
from
(
    select
    t1.product_id
    ,t1.product_name
    ,t1.category
    ,coalesce(t2.q2_2024_sales_total, 0) as q2_2024_sales_total
    ,dense_rank()over(partition by t1.category order by t2.q2_2024_sales_total desc) as category_rank
    ,t3.supplier_name
    from product_info t1
    left join 
    (
        select
        product_id
        ,sum(total_amount) as q2_2024_sales_total
        from order_info 
        where left(order_date, 7) in ('2024-04', '2024-05', '2024-06')
        group by 1
    ) t2
    on t1.product_id = t2.product_id
    left join supplier_info t3
    on t1.product_id = t3.product_id
) tt
order by 1

59. 24年京东-查询出不同类别商品中，销售金额排名前三且利润率超过20%的商品信息
https://www.nowcoder.com/practice/3d70132f4c14442cada25fec0198e743
SQL
select
product_id
,product_name
,category_id
,sales_amount
,profit_rate
from
(
    select
    t1.product_id
    ,t2.product_name
    ,t2.category_id
    ,sum(t1.sales_amount) as sales_amount
    ,round(sum(t1.sales_amount - cost_amount) / sum(t1.sales_amount), 2) as profit_rate
    ,row_number()over(partition by t2.category_id order by sum(t1.sales_amount) desc) as rk
    from sales_and_profit t1
    left join product_category t2
    on t1.product_id = t2.product_id
    group by 1, 2, 3
) tt
where rk <= 3 
and profit_rate > 0.2
order by 3, 4 desc, 1

60. 24年京东-分析每个员工在不同项目中的绩效情况
https://www.nowcoder.com/practice/fa64fd2eb40d4639bc23dfb1ffae2163
SQL
select
t1.employee_id
,t2.employee_name 
,t1.performance_score as first_half_2024_score
,row_number()over(partition by t3.project_id order by t1.performance_score desc, t1.employee_id) as project_group_rank
,t2.department 
,t3.project_name as project_group
from performance t1
left join employees t2
on t1.employee_id = t2.employee_id 
left join projects t3
on t1.project_id = t3.project_id 
where left(t3.start_date , 7) in ('2024-01','2024-02', '2024-03', '2024-04', '2024-05', '2024-06')
order by 6, 4, 1

61. 24年京东-查询出每个品牌在特定时间段内的退货率以及平均客户满意度评分
https://www.nowcoder.com/practice/39f4ccb8ac1b47a89d092b4d8ed08bc8
SQL
select
t1.brand_id
,t1.brand_name
,round(t2.return_rate_July_2024, 2) as return_rate_July_2024
,round(t2.average_customer_satisfaction_score, 2) as average_customer_satisfaction_score
from brand_info t1
left join
(
    select
    a.brand_id
    ,sum(a.return_status) / count(*) as return_rate_July_2024
    ,avg(customer_satisfaction_score) as average_customer_satisfaction_score
    from sales_orders a
    left join customer_feedback b
    on a.order_id = b.order_id
    where left(a.order_date, 7) = '2024-07' 
    group by 1
) t2
on t1.brand_id = t2.brand_id
order by 1

62. 24年京东-物流公司想要分析快递小哥的薪资构成和绩效情况
https://www.nowcoder.com/practice/4be55ba954bf4f928a2d6ff840f23d1b
SQL
select
t1.courier_id
,t1.courier_name 
,t1.base_salary + t2.delivery_fee - t3.expense_amount as total_income
from couriers_info t1
left join
(
    select
    courier_id
    ,sum(delivery_fee) as delivery_fee
    from deliveries_info
    where left(delivery_date, 7) = '2024-07'
    group by 1
) t2
on t1.courier_id = t2.courier_id
left join
(
    select
    courier_id
    ,sum(expense_amount) as expense_amount
    from expenses_info 
    where left(expense_date, 7) = '2024-07'
    group by 1
) t3
on t1.courier_id = t3.courier_id
order by 1

63. 24年京东-查询出每个品牌在不同月份的总销售额以及购买该品牌商品的用户的平均年龄
https://www.nowcoder.com/practice/a50c67d3374f4d0e85869d3e48e02c0a
SQL
select
t1.category_id
,sum(t1.order_amount) as total_sales
,count(distinct case when t2.customer_gender = '男' then t2.customer_id end) as male_customers
,count(distinct case when t2.customer_gender = '女' then t2.customer_id end) as female_customers
from order_details t1
left join customer_info t2
on t1.order_id = t2.order_id
where order_date >= '2024-01-01'
and order_date <= '2024-06-30'
group by t1.category_id
order by t1.category_id

64. 24年京东-电商平台需要对各行业销售情况综合评估
https://www.nowcoder.com/practice/120cbc6f87214886bbba80d2b5414786
SQL
select
t2.industry
,sum(t1.sale_amount) as total_sales_amount
from sales_underline t1
left join merchants_underline t2
on t1.merchant_id = t2.merchant_id
group by t2.industry
order by sum(t1.sale_amount) desc

65. 24年京东-电商平台想要查询出每个商品在2024年上半年（1月至6月）的总销售额
https://www.nowcoder.com/practice/e190c019dabe4622ae719cca64437a47
SQL
select
t1.product_id
,t2.product_name
,sum(t1.quantity * t2.price) as total_sales
from sales_underline t1
left join products_underline t2
on t1.product_id = t2.product_id
where sale_month in ('2024-01', '2024-02', '2024-03','2024-04','2024-05','2024-06')
group by t1.product_id
,t2.product_name
order by t1.product_id

66. 24年京东-电商平台需要对商品的销售和评价情况进行综合分析
https://www.nowcoder.com/practice/ccb441966a0342f2ab5fa8e76c33a3e6
SQL
select
t1.product_id
,t1.product_name
,t2.quantity as total_quantity
,round(t3.rating, 2) as average_rating
from products_underline t1
left join
(
    select
    product_id 
    ,sum(quantity) as quantity
    from sales_underline 
    group by product_id
) t2
on t1.product_id = t2.product_id
left join
(
    select
    product_id
    ,avg(rating) as rating
    from reviews_underline 
    group by product_id
) t3
on t1.product_id = t3.product_id
where t3.rating < 4
order by t3.rating

67. 24年京东-评估2023年不同品牌商品的销售趋势和客户满意度
https://www.nowcoder.com/practice/a32c7ff803054a919e2b65334463002f
SQL
select
t1.brand_id
,sum(t1.sales_amount) as total_sales_amount 
,sum(t1.sales_quantity) as total_sales_quantity 
,round(avg(t2.satisfaction_score), 2) as avg_satisfaction_score 
from sales_data t1
left join customer_feedback t2
on t1.sales_id = t2.sales_id
where left(sales_month, 4) = '2023'
group by t1.brand_id
order by t1.brand_id

68. 24年京东-查询出每个运输方式在不同城市的平均运输时长以及总运输费用
https://www.nowcoder.com/practice/673bf7b17e7c4962bcde889980eec872
SQL
select
t1.destination_city 
,t3.transport_name 
,round(avg(datediff(delivery_date, order_date)), 2) as average_transport_duration
,sum(t2.total_cost) as total_transport_cost
from order_info t1
left join cost_data t2
on t1.order_id = t2.order_id
left join transport_detail t3
on t1.transport_id = t3.transport_id 
group by t1.destination_city 
,t3.transport_name 
order by t1.destination_city 
,t3.transport_name 

69. 24年京东-分析员工在不同项目中的绩效表现以及所属部门的平均绩效情况
https://www.nowcoder.com/practice/20c76a1181004965a3106524fd3ab583
SQL
select
employee_id
,department_name 
,performance_score 
from
(
    select
    t1.employee_id
    ,t1.performance_score 
    ,t2.department_name 
    ,avg(t1.performance_score)over(partition by t2.department_id) as avg_performance_score
    from employee_projects t1
    left join department_info t2
    on t1.employee_id = t2.employee_id
) tt
where performance_score > avg_performance_score
order by employee_id

70. 24年京东-物流公司想要分析快递小哥的收入情况
https://www.nowcoder.com/practice/749ba0168f014c639b516258c0ed6c5d
SQL
select
t1.courier_id
,t1.courier_name
,t1.base_salary + t2.delivery_fee as total_income
from couriers_info t1
left join
(
    select
    courier_id
    ,sum(delivery_fee) as delivery_fee
    from deliveries_info  
    where substr(delivery_date, 1, 7) = '2024-07'
    group by courier_id
) t2
on t1.courier_id = t2.courier_id
order by t1.courier_id

71. 24年京东-分析不同门店各类商品的库存情况和销售情况
https://www.nowcoder.com/practice/5b9262a36724466ea1ae1f58187197d6
SQL
select
t1.store_id
,t2.store_name
,t3.product_category
,t1.inventory_quantity
,t1.sales_amount 
from sales_inventory t1
left join stores t2
on t1.store_id = t2.store_id
left join products t3
on t1.product_id = t3.product_id 
where t1.inventory_quantity < 10
and sales_amount > 5000
order by t1.store_id, t3.product_id

72. 24年京东-评估不同供应商提供的零部件质量和成本情况
https://www.nowcoder.com/practice/dc44fdd330e8429db8271efc38ce1922
SQL
select
t1.supplier_id
,t2.supplier_name
,t3.component_name
,t1.quality_score
,t1.cost
from supply_quality_cost t1
left join suppliers t2
on t1.supplier_id = t2.supplier_id 
left join components t3
on t1.component_id = t3.component_id
where t1.quality_score > 80 
and t1.cost < 50
order by t1.supplier_id
,t1.cost

73. 24年京东-了解2023年全年所有商品的盈利情况
https://www.nowcoder.com/practice/05cbbb8662c14b46a15cbcb8993d9277
SQL
select
t1.product_id
,sum((t1.unit_price - t2.purchase_price) * t1.quantity) as total_profit
,round((avg(t1.unit_price) - max(t2.purchase_price)) / max(t2.purchase_price) * 100, 2) as profit_margin 
from sales_orders t1
left join purchase_prices t2
on t1.product_id = t2.product_id
where left(order_date, 4) = '2023'
group by t1.product_id
order by t1.product_id

74. 24年京东-哪些产品在特定时间段内表现最为出色
https://www.nowcoder.com/practice/866a4614615b43a29750537ede4bf0c8
SQL
select
product_id
,product_name
,total_sales_amount
,total_sales_quantity
from
(
    select
    t1.product_id
    ,t2.product_name
    ,sum(t1.sales_amount) as total_sales_amount
    ,sum(sales_quantity) as total_sales_quantity
    ,dense_rank()over(order by sum(sales_quantity) desc) as rk
    from sales_records t1
    left join products t2
    on t1.product_id = t2.product_id
    where left(t1.sales_date, 4) = '2024'
    group by t1.product_id
    ,t2.product_name
) tt
where rk = 1
order by product_id

75. 24年饿了么-分析配送员的配送效率
https://www.nowcoder.com/practice/e27ba25e7722478eb86c832fab96fc1a
SQL
select
t2.weather_type
,round(avg(t1.delivery_time), 2) as average_delivery_time
,count(*) as delivery_count
from delivery_records t1
left join weather_conditions t2
on t1.weather_id = t2.weather_id
where staff_id in (
    select distinct
    a.staff_id
    from delivery_staff a
    left join
    (
        select
        staff_id
        ,sum(is_complaint) / count(*) as complaint_rate
        from delivery_records
        group by staff_id
    ) b
    on a.staff_id = b.staff_id
    where a.average_speed > 20
    and b.complaint_rate < 0.5
)
group by t2.weather_type
order by t2.weather_type

76. 24年OPPO-深入分析各款产品年总销售额与竞品的年度对比
https://www.nowcoder.com/practice/99cc7f1798a84645a6aca5bdfd163fdb
SQL
select
t1.product_id 
,t1.product_name 
,t3.competitor_name 
,t2.total_sales_amount_of_product
,t2.total_sales_amount_of_product - t3.total_competitor_sales_amount_2023 as sales_difference_with_competitor
from oppo_products_detail t1
left join 
(
    select
    product_id 
    ,sum(quarter_1_sales_amount + quarter_2_sales_amount + quarter_3_sales_amount + quarter_4_sales_amount) as total_sales_amount_of_product
    from sales_info
    group by product_id
) t2
on t1.product_id = t2.product_id
left join competitor_analysis t3
on t1.product_id = t3.product_id
order by t1.product_id 

77. 24年OPPO-分析各产品线在特定时间段内的销售情况
https://www.nowcoder.com/practice/8a002dd7888b4247b6ac9228577bdbc3
SQL
select
t2.product_line
,t3.region
,t3.channel_name
,sum(t1.sale_amount) as total_sale_amount
,count(*) as total_sale_quantity
from sales_data t1
left join oppo_products t2
on t1.product_id = t2.product_id
left join sales_channels t3
on t1.channel_id = t3.channel_id
group by t2.product_line
,t3.region
,t3.channel_id
,t3.channel_name
order by t2.product_line, t3.channel_id

78. 25年携程-查询高价值旅行套餐客户的支出与套餐详情
https://www.nowcoder.com/practice/957e8ab30e2745b48d2f79046df73a23
SQL
select
t3.name as customer_name
,sum(t2.price) as total_travel_cost
,count(*) as order_count
,round(sum(t2.price) / count(*), 2) as avg_order_price
from bookings t1
left join packages t2
on t1.package_id = t2.id
left join customers t3
on t1.customer_id = t3.id
where left(booking_date, 4) = '2024'
group by t3.name
having sum(t2.price) > 10000
order by sum(t2.price) desc

79. 24年蚂蚁-贷款情况
https://www.nowcoder.com/practice/2817d353f0634208bcf0de74f56ca8f0
SQL
select
tt1.city
,round(tt1.total_loan_amount, 2) as total_loan_amount
,round(tt1.average_loan_amount, 2) as average_loan_amount
,round(tt1.total_customers, 2) as total_customers
,tt2.loan_type_name as most_applied_loan_type
from
(
    select
    t2.city
    ,sum(t1.loan_amount) as total_loan_amount
    ,sum(t1.loan_amount) / count(distinct t1.customer_id) as average_loan_amount
    ,count(distinct t1.customer_id) as total_customers
    from loan_applications t1
    left join customers t2
    on t1.customer_id = t2.customer_id
    group by t2.city
) tt1
left join
(
    select
    t2.city
    ,t3.loan_type_id
    ,t4.loan_type_name
    ,count(*) as cnt
    ,row_number()over(partition by t2.city order by count(*) desc, t3.loan_type_id) as rk
    from loan_applications t1
    left join customers t2
    on t1.customer_id = t2.customer_id
    left join loan_application_types t3
    on t1.application_id = t3.application_id
    left join loan_types t4
    on t3.loan_type_id = t4.loan_type_id
    group by t2.city
    ,t3.loan_type_id
    ,t4.loan_type_name
) tt2
on tt1.city = tt2.city
and tt2.rk = 1
order by tt1.city

80. 24美团-统计借阅量
原题链接：https://www.nowcoder.com/practice/280ed56ab3ee49a4b2a4595d38e1d565
SQL
select
t1.book_id
,t1.book_title
,coalesce(feb_2023_borrows, 0) as feb_2023_borrows
,coalesce(feb_2024_borrows, 0) as feb_2024_borrows
,coalesce(jan_2024_borrows, 0) as jan_2024_borrows
,coalesce(yoy_delta, 0) as yoy_delta
,coalesce(mom_delta, 0) as mom_delta
,coalesce(north_pct_2023, 0) as north_pct_2023
,coalesce(south_pct_2023, 0) as south_pct_2023
,coalesce(east_pct_2023, 0) as east_pct_2023
from Books t1
left join 
(
    select
    a.book_id
    ,sum(case when left(a.borrow_date, 7) = '2023-02' then 1 else 0 end) as feb_2023_borrows
    ,sum(case when left(a.borrow_date, 7) = '2024-02' then 1 else 0 end) as feb_2024_borrows
    ,sum(case when left(a.borrow_date, 7) = '2024-01' then 1 else 0 end) as jan_2024_borrows
    ,sum(case when left(a.borrow_date, 7) = '2024-02' then 1 else 0 end) - sum(case when left(a.borrow_date, 7) = '2023-02' then 1 else 0 end) as yoy_delta
    ,sum(case when left(a.borrow_date, 7) = '2024-02' then 1 else 0 end) - sum(case when left(a.borrow_date, 7) = '2024-01' then 1 else 0 end) as mom_delta
    ,round(sum(case when left(a.borrow_date, 4) = '2023' and b.region in ('华北') then 1 else 0 end) / sum(case when left(a.borrow_date, 4) = '2023' then 1 else 0 end) * 100, 2) as north_pct_2023
    ,round(sum(case when left(a.borrow_date, 4) = '2023' and b.region in ('华南') then 1 else 0 end) / sum(case when left(a.borrow_date, 4) = '2023' then 1 else 0 end) * 100, 2) as south_pct_2023
    ,round(sum(case when left(a.borrow_date, 4) = '2023' and b.region in ('华东') then 1 else 0 end) / sum(case when left(a.borrow_date, 4) = '2023' then 1 else 0 end) * 100, 2) as east_pct_2023
    from BorrowRecords a
    left join Branches b
    on a.branch_id = b.branch_id
    group by a.book_id
) t2
on t1.book_id = t2.book_id
order by t1.book_id, t1.book_title

81. 24美团-统计骑手信息
原题链接：https://www.nowcoder.com/practice/704de2445ed943c6bf65cfd77bd69ff4
SQL
select
t1.zone_id
,t1.zone_name 
,t2.peak_2023_02_delivered
,t2.peak_2024_02_delivered
,t2.peak_2024_01_delivered
,t2.yoy_delta
,t2.mom_delta
,round(t2.avg_peak_minutes_2024_02, 2) as avg_peak_minutes_2024_02
,t3.courier_name as top_courier_2024_02
from Zones t1
left join
(
    select
    zone_id
    ,sum(case when left(order_time, 7) in ('2023-02') then 1 else 0 end) as peak_2023_02_delivered
    ,sum(case when left(order_time, 7) in ('2024-02') then 1 else 0 end) as peak_2024_02_delivered
    ,sum(case when left(order_time, 7) in ('2024-01') then 1 else 0 end) as peak_2024_01_delivered
    ,sum(case when left(order_time, 7) in ('2024-02') then 1 else 0 end) - sum(case when left(order_time, 7) in ('2023-02') then 1 else 0 end) as yoy_delta
    ,sum(case when left(order_time, 7) in ('2024-02') then 1 else 0 end) - sum(case when left(order_time, 7) in ('2024-01') then 1 else 0 end) as mom_delta
    ,avg(case when left(order_time, 7) in ('2024-02') then TIMESTAMPDIFF(minute, order_time, delivered_time) end) as avg_peak_minutes_2024_02
    from Orders
    where ((hour(order_time) BETWEEN 11 AND 13) OR (hour(order_time) BETWEEN 18 AND 20))
    and status = 'delivered'
    group by zone_id
) t2
on t1.zone_id = t2.zone_id
left join
(
    select
    a.zone_id
    ,a.courier_id
    ,b.courier_name 
    ,count(*) as cnt
    ,row_number()over(partition by a.zone_id order by count(*) desc, a.courier_id) as rk
    from Orders a
    left join Couriers b 
    on a.courier_id = b.courier_id
    where ((hour(order_time) BETWEEN 11 AND 13) OR (hour(order_time) BETWEEN 18 AND 20))
    and left(a.order_time, 7) in ('2024-02')
    and a.status = 'delivered'
    group by a.zone_id
    ,a.courier_id
    ,b.courier_name 
) t3
on t1.zone_id = t3.zone_id
and t3.rk = 1
order by t1.zone_id
,t1.zone_name 

