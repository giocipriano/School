/* LAB 1 for Abrera, Hal | Cipriano, Gio | Imperial, Audi */

/* number 1 */

select 

    dest, carrier_desc, arr_delay_new, dep_delay_new
    
    from performance, codes_carrier
    where
    carrier_code = mkt_carrier and arr_delay_new > dep_delay_new;
    
select 
    diverted, 
    from performance
    where
    diverted > 0;
    
/* number 2 */
    

with 

avg_delaysfo as 
(
select dest, avg(dep_delay_new) as avgmonthdelayforSFO
from performance
where dest = 'SFO'
group by dest  
)
,
avg_delayord as 
(
select dest, avg(dep_delay_new) as avgmonthdelayforORD
from performance
where dest = 'ORD'
group by dest  
)

select performance.mkt_carrier, performance.dest, performance.dep_delay_new, avg_delaysfo.avgmonthdelayforSFO, avg_delayord.avgmonthdelayforORD
from performance, avg_delaysfo, avg_delayord
where performance.dep_delay_new > avg_delaysfo.avgmonthdelayforSFO and
performance.dep_delay_new > avg_delayord.avgmonthdelayforORD and
performance.dest in ('SFO', 'ORD') and
performance.mkt_carrier = 'UA'
group by performance.mkt_carrier, performance.dest, performance.dep_delay_new, avg_delaysfo.avgmonthdelayforSFO, avg_delayord.avgmonthdelayforORD;


/* number 3 */

create or replace function show_alliance(in bruh text, out partner text) as $$
begin
    case
        when bruh = 'AA' then partner:='One World';
        when bruh = 'DL' then partner:='SkyTeam';
        when bruh = 'HA' then partner:='Star Alliance';
        when bruh = 'UA' then partner:='Star Alliance';
        when bruh in ('AS', 'B6', 'F9', 'G4', 'NK', 'VX', 'WN') then partner:= 'No Alliance';
    end case;
end;

$$ language plpgsql;

select mkt_carrier_fl_num, mkt_carrier, show_alliance(mkt_carrier) from performance;