with
    ratings as (
        select work, rating, `date` from `open-library-pipeline.open_library.ratings`
    )
select *
from ratings
