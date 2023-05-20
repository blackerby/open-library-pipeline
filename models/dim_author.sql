with stg_authors as (select author_key, name from {{ ref("stg_authors") }})
select
    {{ dbt_utils.generate_surrogate_key(["stg_authors.author_key"]) }} as author_id,
    stg_authors.author_key,
    stg_authors.name
from stg_authors
