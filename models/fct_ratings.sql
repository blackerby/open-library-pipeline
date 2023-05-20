with
    stg_ratings as (
        select work as work_key, rating, `date` as rating_date
        from {{ ref("stg_ratings") }}
    ),
    stg_works as (
        select `key` as work_key, subjects, author from {{ ref("stg_works") }}
    ),
    stg_subjects as (
        select work_key, subject from stg_works cross join unnest(subjects) as subject
    )
select
    {{
        dbt_utils.generate_surrogate_key(
            ["stg_works.work_key", "stg_ratings.work_key"]
        )
    }} as rating_id,
    {{ dbt_utils.generate_surrogate_key(["stg_works.work_key"]) }} as work_id,
    {{ dbt_utils.generate_surrogate_key(["stg_works.author"]) }} as author_id,
    {{ dbt_utils.generate_surrogate_key(["stg_subjects.subject"]) }} as subject_id,
    stg_ratings.rating,
    stg_ratings.rating_date
from stg_ratings
join stg_works
join
    stg_subjects
    on stg_subjects.work_key = stg_works.work_key
    on stg_works.work_key = stg_ratings.work_key
