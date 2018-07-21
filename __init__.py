try:
    import yahoo_auction
    import google_image_search
except (Exception, ) as e:
    from . import yahoo_auction
    from . import google_image_search
