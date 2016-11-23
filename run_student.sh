#!/usr/bin/env bash

echo '----------------------------------------'
echo '>>>>>>>>>>>>>>>>>>> start : ' `date`
START_TIME=`date +%s`

DATE=$1
if [ -z ${DATE} ]; then
    DATE=`date -d '-1 day' +%Y%m%d`
fi

YEAR=`date -d ${DATE} +%Y`
MONTH=`date -d ${DATE} +%m`
DAY=`date -d ${DATE} +%d`

DATE_PARTITION=${YEAR}/${MONTH}/${DAY}
OUTPUT_HDFS_PATH="/user/rd/dm/student/${DATE_PARTITION}"
HOME_SQL="select * from dm.passenger_home_company_residence_V2 where concat(year,month,day)='${DATE}'"
EDU_IP_SQL="select pid, weekday_edu_nums, weekend_edu_nums from dm.passenger_eduip_feature where weekday_edu_nums >= '1' or weekend_edu_nums >= '1' and concat(year,month,day)='20161120'"
USER_INFO_SQL="select uid,
                  corp,
                  employ,
                  trade_id,
                  age
           from pdw.userinfo
           where uid is not null and concat(year, month, day) = '${DATE}' and channel <> 1"
STUDENT_8090S_SQL="select uid, cardid, age_level from pdw.userinfo where concat(year,month,day)='${DATE}' and (length(trim(cardid))=18 or age_level='4.0' or age_level='3.0') and auth_state in(2,4,5,6,7)"
EDU_INSTITUTION_DICT_DIR="/user/rd/dm/xiejun/coord_education_institution/2016/11/21"

hadoop fs -rm -r ${OUTPUT_PATH}

hive -e "
alter table dm.student add if not exists partition(year='${YEAR}', month='${MONTH}', day='${DAY}') location \"${OUTPUT_PATH}\";
"
spark-submit    --driver-memory 4g \
                --conf "spark.dynamicAllocation.minExecutors=50" \
                --conf "spark.dynamicAllocation.maxExecutors=200" \
                --conf spark.sql.shuffle.partitions=1000 \
                --conf spark.akka.frameSize=1000 \
                --conf spark.storage.memoryFraction=0.5 \
                --conf spark.default.parallelism=9600 \
                --num-executors 300 \
                --queue root.dashujudidiyanjiuyuan-zhinengpingtaibu.profile \
                --class passenger.profile.stable.occupation.student.Student \
                intelli-dm-1.0-jar-with-dependencies.jar \
                --output_hdfs_path "${OUTPUT_HDFS_PATH}" \
                --user_info_sql "${USER_INFO_SQL}" \
                --home_residence_sql "${HOME_SQL}" \
                --student_8090s_sql "${STUDENT_8090S_SQL}" \
                --edu_ip_sql "${EDU_IP_SQL}" \
                --education_institution_dict_dir "${EDU_INSTITUTION_DICT_DIR}" \
                --data_date "${YEAR}${MONTH}${DAY}" \


END_TIME=`date +%s`
echo 'Output Path : ' ${OUTPUT_PATH}
echo '******************** Total Cost : ' $(( END_TIME-START_TIME)) 'seconds!'
echo '>>>>>>>>>>>>>>>>>>>> end : ' `date`
echo -e '---------------------------------------- \n'
