with
    stg_works as (
        select `key` as work_key, subjects, author from {{ ref("stg_works") }}
    ),
    stg_subjects as (
        select work_key, subject, author
        from stg_works
        cross join unnest(subjects) as subject
    )
select
    {{ dbt_utils.generate_surrogate_key(["stg_subjects.subject"]) }} as subject_id,
    stg_subjects.subject,
    {{ dbt_utils.generate_surrogate_key(["stg_subjects.work_key"]) }} as work_id,
    stg_subjects.work_key,
    {{ dbt_utils.generate_surrogate_key(["stg_subjects.author"]) }} as author_id,
    stg_subjects.author as author_key
from stg_subjects
