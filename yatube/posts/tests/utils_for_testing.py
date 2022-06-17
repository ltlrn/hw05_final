from math import ceil


def posts_per_page_for_test(name, number_of_posts, posts_per_page):
    """Создание словаря адресов для проверки страниц паджинатора."""

    if number_of_posts < posts_per_page:
        posts_per_page = number_of_posts

    test_dict = {name: posts_per_page}

    if number_of_posts > posts_per_page:
        pages_required = ceil(number_of_posts / posts_per_page)

        for page in range(2, pages_required + 1):
            number = posts_per_page
            if page == pages_required:
                number = number_of_posts % posts_per_page

            test_dict[f'{name}' + f'?page={page}'] = number

    return test_dict


def create_test_dicts_list(names_list, number_of_posts, posts_per_page):
    """Создание списка словарей адресов для проверки страниц с паджинацией."""

    test_dicts = []
    for name in names_list:
        test_dicts.append(
            posts_per_page_for_test(
                name,
                number_of_posts,
                posts_per_page,
            )
        )

    return test_dicts
