with
    ratings as (
        select work, shelf, `date` from `open-library-pipeline.open_library.reading-log`
    )
select *
from ratings
