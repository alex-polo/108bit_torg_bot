import aiogram.utils.markdown as fmt

"""
start = State()
    city = State()
    type_task = State()
    type_equipment_consumables = State()
    vendor = State()
    count = State()
    condition = State()
    # salesman = State()
    # price = State()
    # payment_type = State()
    # sending_to_another_city = State()
    # email = State()
    # phone = State()
    # details = State()
    # photo = State()
    publish = State()
    finish = State()
"""
def post_message(data: dict) -> tuple:
    date = fmt.hbold(post.date.strftime("%d-%m-%Y"))
    tags = fmt.hunderline(f'{post.main_tag} {"  ".join(post.field_tags.split(","))} {post.author}')
    title = fmt.hbold(post.title)
    details = post.details

    # keyboard = get_keyboard_more('🔎  Подробнее', url=post.more)
    more_tag = fmt.hlink('🔎  Подробнее', post.more)

    date_body = fmt.text(date)
    body = fmt.text(
        fmt.text(tags),
        fmt.text(title),
        fmt.text(details),
        more_tag,
        sep="\n\n")

    image_content: ImageContent = formatting_image(url=post.image_url, path_main_image=path_main_image)

    # return post.id, fmt.text(date_body, body, sep="\n"), image_content, keyboard
    return post.id, fmt.text(date_body, body, sep="\n"), image_content
