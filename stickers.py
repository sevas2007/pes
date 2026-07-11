import random
bad_sticker_ids = set()
shiba_stickers = {
    "позитив": [
        "CAACAgIAAxUAAWpREceMe24Gt1JIzGDHPfluCLNRAAITkwACV1-oSZ-A7gbByCP8PAQ",
        "CAACAgIAAxUAAWpREcfgA9CEI_XWT8HO8sbqCnhgAAJJnAACAna4SiYyvl56xHzsPAQ",
        "CAACAgIAAxUAAWpREcfoNbd34SvILTQjfwkfrTGDAAK6rAACTqhxS0IClAHsqvbwPAQ",
        "CAACAgIAAxUAAWpREce-NkIf18mPj4Vj8seXhn_0AAKyowACsjyhS3zTNPi5GUhrPAQ",
        "CAACAgIAAxUAAWpREcdTQmb7jL5290NB542ETgmxAAIimQACuLB4SgYPgmRwpp9kPAQ",
        "CAACAgIAAxUAAWpREceJ5gKE969fWcB7_K9xkn-BAAIVmgACEKZhSqpnyb0LPQLBPAQ",
        "CAACAgIAAxUAAWpREceLCKoGVjwdXs_M9KH0TIO0AALBkgACm7wxSjRMsP9zI88OPAQ",
        "CAACAgIAAxUAAWpREcdEeE3aHBiXk2OHhLIpe1UEAALEqQACULhoSDci5qQ6HwaNPAQ",
        "CAACAgIAAxUAAWpREccCJJyH_hBwX8RPKIK7jspLAAJakgAC3pxxSwLES_WBgcifPAQ",
        "CAACAgIAAxUAAWpREcdqf9ZFigQcRy5vrvFsdl-NAAK4nAACufkJSZVET0482YyCPAQ",
        "CAACAgIAAxUAAWpREceo4cWw9x3xJ6bJ7Q6hK0cAAK7mQACjyJISwGzK6z3b1rQPAQ"
    ],
    "веселость": [
        "CAACAgIAAxUAAWpREccb3s7Qx1hJz8b4k6wW7f9qAAJ4mwAC7xZJSYj7x4Jjv3ZrPAQ",
        "CAACAgIAAxUAAWpREcebZctoqRlVU9aNoHiB_tsGAAK8kAACL764Sem75mLi8oElPAQ",
        "CAACAgIAAxUAAWpREcexpZgeFKvJYG_w6KNNDtPIAAIpmwAC0RxYStxMIEtBsEmFPAQ",
        "CAACAgIAAxUAAWpREccQv7z2u3xQy7W4lP6kQ3gAAJ4ngAC0hQ5Sy9p4jZ9cZkqPAQ"
    ],
    "неприязнь": [
        "CAACAgIAAxUAAWpREcedQRZCvuPeX0CbWL4_YpoLAAJnhwACJq9RSlYDgMTeZ3NaPAQ",
        "CAACAgIAAxUAAWpREceQayTvQ-IeKCuR_aus371yAALMmQACKqHISX82IqDyQvVtPAQ",
        "CAACAgIAAxUAAWpREcdky-IVKyp2kAgLB5OYNP6HAALdngAClpXZSbn7xU_LkuaYPAQ"
    ],
    "вопрос": [
        "CAACAgIAAxUAAWpREceH_d61B6wuzY02Q8nhstrJAAJ0oAACKuyoSVHzbmH1qbqEPAQ",
        "CAACAgIAAxUAAWpREceLCKoGVjwdXs_M9KH0TIO0AALBkgACm7wxSjRMsP9zI88OPAQ",
        "CAACAgIAAxUAAWpREceNSkdBXDyTKIW6FVADO-kxAAKMmQACN2a5SSUuztIdxcnAPAQ",
        "CAACAgIAAxUAAWpREccSH1DuE6zDKg0oeT5rBmYJAAJ0kgACdZixSdVFEXGJ7qvCPAQ"
    ],
    "голод": [
        "CAACAgIAAxUAAWpREcdajmKhDXbtBXsXd9N6VU6uAAK2nwACkRC5Skj6kya5o57BPAQ"
    ],
    "спорт": [
        "CAACAgIAAxUAAWpREceH_d61B6wuzY02Q8nhstrJAAJ0oAACKuyoSVHzbmH1qbqEPAQ",
        "CAACAgIAAxUAAWpREcetfNXa9yIXYjjvLO1fymQ5AALnmwACtmvISeR_DJO97ZidPAQ",
        "CAACAgIAAxUAAWpREcdmEcaGUPmdOdJKy8WJWrHJAAJXngACbUzgSQes_eDNQQQ6PAQ",
        "CAACAgIAAxUAAWpREcfGrRJD7YRnhzuZzHTmgbeOAAJFoAACBmkQSOul6t77136qPAQ"
    ]
}
ALL_SHIBA_STICKERS = ['CAACAgIAAxUAAWpREceNE_7yyYgC_MvIzbfwbj-oAAKEkAACSuq4STfs1n8BCFmgPAQ', 
                  'CAACAgIAAxUAAWpREcedQRZCvuPeX0CbWL4_YpoLAAJnhwACJq9RSlYDgMTeZ3NaPAQ', 
                  'CAACAgIAAxUAAWpREceH_d61B6wuzY02Q8nhstrJAAJ0oAACKuyoSVHzbmH1qbqEPAQ', 
                  'CAACAgIAAxUAAWpREccmUAbTn47sPYq2JqysLqGnAALumgACSGmoSb8WgCtGUHlPPAQ', 
                  'CAACAgIAAxUAAWpREccSH1DuE6zDKg0oeT5rBmYJAAJ0kgACdZixSdVFEXGJ7qvCPAQ', 
                  'CAACAgIAAxUAAWpREccZgaf52Z3QW0c0bvPTHMueAAIRmAACjnfISWZBLMGLGfO5PAQ', 
                  'CAACAgIAAxUAAWpREcfgEwcAAWjTAQyLNv2TG0IzKQACK5IAAt1LyUlhT69yj8CIHDwE', 
                  'CAACAgIAAxUAAWpREccNSkdBXDyTKIW6FVADO-kxAAKMmQACN2a5SSUuztIdxcnAPAQ', 
                  'CAACAgIAAxUAAWpREcfzDuW_BinRrEDEzOJa61V4AAL9mQACH2S4SVfAGHC5h_G7PAQ', 
                  'CAACAgIAAxUAAWpREcebZctoqRlVU9aNoHiB_tsGAAK8kAACL764Sem75mLi8oElPAQ', 
                  'CAACAgIAAxUAAWpREcdn0KTRQmVNKQlWkLK_s5F8AAI0qAACFmKhSSQi5YwcRzWoPAQ', 
                  'CAACAgIAAxUAAWpREce8d6s3g_yxxSbEVEeFf41XAALungACJhi5SfKEC1XmojsxPAQ', 
                  'CAACAgIAAxUAAWpREcdEO4l7S2KPSV99dVwUSRjnAALklAACjTvJScR-6IJD4EMkPAQ', 
                  'CAACAgIAAxUAAWpREcfqSJYW8x11r7k6_xfNkNKYAAK-lwACOotBSi9Vwjs4BrdPPAQ', 
                  'CAACAgIAAxUAAWpREcfOOsDGhuHyuEEkM3T7sPcoAALkigAC3daoSfVhXRbKnUcsPAQ', 
                  'CAACAgIAAxUAAWpREcfgA9CEI_XWT8HO8sbqCnhgAAJJnAACAna4SiYyvl56xHzsPAQ', 
                  'CAACAgIAAxUAAWpREcepb1LyMTD5k2pYS_UMCu_SAAJ7mQAC36DIS7btcmWIWsnNPAQ', 
                  'CAACAgIAAxUAAWpREccrN-H3M9NeZ7T_STCYinThAAJZngACMxuIS0rzZ6Dd3nPQPAQ', 
                  'CAACAgIAAxUAAWpREccii1Ekj0dX1_eMOVbnVevwAALomgACSX1hSpPPYOt5LfC9PAQ', 
                  'CAACAgIAAxUAAWpREccLyx-Z44_UZLA3XMAUB4nCAAKtmAACVejgSe8o-EkaWSYSPAQ', 
                  'CAACAgIAAxUAAWpREcetfNXa9yIXYjjvLO1fymQ5AALnmwACtmvISeR_DJO97ZidPAQ', 
                  'CAACAgIAAxUAAWpREcfEv8zdyNfh_5UUB50Sw2bCAALmmgACFvnJSadQ71OwT8GQPAQ', 
                  'CAACAgIAAxUAAWpREce7HNeEnKhaD1PzB4pMY26UAAI5kgACenyoScf53sov-eDGPAQ', 
                  'CAACAgIAAxUAAWpREccfoN09P1Szgcc2-hxn8KeXAAJyqwAC23iBSyOKHRkhVUiTPAQ', 
                  'CAACAgIAAxUAAWpREccQayTvQ-IeKCuR_aus371yAALMmQACKqHISX82IqDyQvVtPAQ', 
                  'CAACAgIAAxUAAWpREcentJdwjb-KjguRtMrtGXp9AALNlgAC3xSpSxzLHd0ufvSlPAQ', 
                  'CAACAgIAAxUAAWpREceMe24Gt1JIzGDHPfluCLNRAAITkwACV1-oSZ-A7gbByCP8PAQ', 
                  'CAACAgIAAxUAAWpREcflL8IQtk_PWXtQZfU0jQRcAAIvnAACXOXASbwkLKfUfUhHPAQ', 
                  'CAACAgIAAxUAAWpREccPVtMabgAB9c4K1FKpW4_GpgACS6QAAr3nKUq-pkJLPVRnnzwE', 
                  'CAACAgIAAxUAAWpREceEJzIuojH4zec0vdItZhY-AAL5ogACkx6hSeFDlNvT2iRJPAQ', 
                  'CAACAgIAAxUAAWpREcfos-7d_0GhF0c0hIrbYbnTAAJtlQACENfYSW6SdSmBPSamPAQ', 
                  'CAACAgIAAxUAAWpREceEoGFBLgjb8hXY8jQo4_GzAAIEnQACE2ShSRSwd8zoQN8BPAQ', 
                  'CAACAgIAAxUAAWpREcdky-IVKyp2kAgLB5OYNP6HAALdngAClpXZSbn7xU_LkuaYPAQ', 
                  'CAACAgIAAxUAAWpREceJ5gKE969fWcB7_K9xkn-BAAIVmgACEKZhSqpnyb0LPQLBPAQ', 
                  'CAACAgIAAxUAAWpREcezt8cPpFmsfSdqvXNohBLvAAJplwACi_KISxZEUtAa8ae3PAQ', 
                  'CAACAgIAAxUAAWpREcfY4OcMjF-1TKp-1FBN7Qw0AAJxnQAC3uiwS11RAjqI5siiPAQ', 
                  'CAACAgIAAxUAAWpREceUcx1e4OKFd2B4Nk4qJs0kAAKdkAACiOPRSowvKj5E07usPAQ', 
                  'CAACAgIAAxUAAWpREcdtY-_yAk8SFTr5eG5Zci4-AAJilwAC6rrZSR77I7k9JUWFPAQ', 
                  'CAACAgIAAxUAAWpREceTbW-UbAV1e3hOT7OhqA_KAAKkngACn3nZSeFP06q0DGnQPAQ', 
                  'CAACAgIAAxUAAWpREcdajmKhDXbtBXsXd9N6VU6uAAK2nwACkRC5Skj6kya5o57BPAQ', 
                  'CAACAgIAAxUAAWpREcdmEcaGUPmdOdJKy8WJWrHJAAJXngACbUzgSQes_eDNQQQ6PAQ', 
                  'CAACAgIAAxUAAWpREceLCKoGVjwdXs_M9KH0TIO0AALBkgACm7wxSjRMsP9zI88OPAQ', 
                  'CAACAgIAAxUAAWpREcdTQmb7jL5290NB542ETgmxAAIimQACuLB4SgYPgmRwpp9kPAQ', 
                  'CAACAgIAAxUAAWpREcdgMMcnfZeYRUSiypRvzwgnAAKJngACX-1ISvhgxIYUgKqCPAQ', 
                  'CAACAgIAAxUAAWpREccvVf8OWJAnPD2ZNYL-sbwSAAOkAAK36thL_zniWrdOx708BA',
                  'CAACAgIAAxUAAWpREcc_XFc85FUiyCtHVuC4NmtwAAJFmAACq6I5S3138nXwe0hrPAQ', 
                  'CAACAgIAAxUAAWpREcdFyuvmwZM2tbM3aRf_4p8FAAK6mwACYPt4S-mH4QdYqgicPAQ', 
                  'CAACAgIAAxUAAWpREce-NkIf18mPj4Vj8seXhn_0AAKyowACsjyhS3zTNPi5GUhrPAQ', 
                  'CAACAgIAAxUAAWpREccCJJyH_hBwX8RPKIK7jspLAAJakgAC3pxxSwLES_WBgcifPAQ', 
                  'CAACAgIAAxUAAWpREcfoNbd34SvILTQjfwkfrTGDAAK6rAACTqhxS0IClAHsqvbwPAQ', 
                  'CAACAgIAAxUAAWpREcexpZgeFKvJYG_w6KNNDtPIAAIpmwAC0RxYStxMIEtBsEmFPAQ', 
                  'CAACAgIAAxUAAWpREcdTTEn5x0g2scQtWo8Fox6YAAKKnQACW-_wSzoqRtZujbggPAQ', 
                  'CAACAgIAAxUAAWpREce3Ug1WDDyQWy6kfEyJp57AAALbmQAC1Ef5S-Gd18sLLE8tPAQ', 
                  'CAACAgIAAxUAAWpREcde3-4M0FI1_fZcgWukJgJ5AAJvnQACne0RSAxh-N2P9PHvPAQ', 
                  'CAACAgIAAxUAAWpREcfGrRJD7YRnhzuZzHTmgbeOAAJFoAACBmkQSOul6t77136qPAQ', 
                  'CAACAgIAAxUAAWpREcd_o8pVn_mrcRVfFv5w_F_yAAK-sQACt40pSJcpQTLHsWu8PAQ', 
                  'CAACAgIAAxUAAWpREcdEeE3aHBiXk2OHhLIpe1UEAALEqQACULhoSDci5qQ6HwaNPAQ', 
                  'CAACAgIAAxUAAWpREcfdd3PTr51YL2exB-YMRGEdAAJDlQACWUdpSDSucP78D6DnPAQ', 
                  'CAACAgIAAxUAAWpREcfm06VdK8e0Hygjbb7JMBhBAAJamgACHOkBSaRrw_D7qLR0PAQ', 
                  'CAACAgIAAxUAAWpREcdqf9ZFigQcRy5vrvFsdl-NAAK4nAACufkJSZVET0482YyCPAQ', 
                  'CAACAgIAAxUAAWpREccHqGThbkoMDLhBKa1fmQbZAAKfowACje3JSaM2L0EoHn9jPAQ', 
                  'CAACAgIAAxUAAWpREcfB-oOTEk7LiVPCPyYVBVHDAAJanwACgIvxSTLLaOBaZ2nqPAQ', 
                  'CAACAgIAAxUAAWpREceuWBXp-cFHTrJJrbI4LxJBAAIPpwACnSr4SXVnC5yXVGKrPAQ', 
                  'CAACAgIAAxUAAWpREcdqrUA0_gxVSl8EiiL9dDJ-AAIPowACDB2ASl13k3Tj63YMPAQ', 
                  'CAACAgIAAxUAAWpREceUKVflJW4KITlQWx79k2auAAJpoQACu9GJSqG_GJEaQxVePAQ'
]

all_stickers = [s for sublist in shiba_stickers.values() for s in sublist]

import random

def get_sticker(category=None):
    def get_safe_choice(items):
        # Перемешиваем, чтобы каждый раз был разный выбор
        shuffled = list(items)
        random.shuffle(shuffled)
        
        for candidate in shuffled:
            clean_id = candidate.strip()
            # Пропускаем, если ID в черном списке
            if clean_id in bad_sticker_ids:
                continue
            # Базовая проверка длины
            if len(clean_id) > 20:
                return clean_id
        return None

    if category and category in shiba_stickers and shiba_stickers[category]:
        if random.random() < 0.60:
            return get_safe_choice(shiba_stickers[category])
            
    if 'all_stickers' in globals() and all_stickers and random.random() < 0.05:
        return get_safe_choice(all_stickers)
        
    return None