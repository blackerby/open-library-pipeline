with
    stg_works as (
        select `key` as work_key, title, subjects, author from {{ ref("stg_works") }}
    )
select
    {{ dbt_utils.generate_surrogate_key(["stg_works.work_key"]) }} as work_id,
    stg_works.work_key,
    stg_works.title,
    stg_works.subjects,
    {{ dbt_utils.generate_surrogate_key(["stg_works.author"]) }} as author_id,
    stg_works.author as author_key
from stg_works
