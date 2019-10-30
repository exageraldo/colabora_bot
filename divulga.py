import random

import gspread

from autenticadores import google_api_auth


def google_sshet():
    """
    Função simples para retornar um objeto capaz de manipular as planilhas do Google Sheets.
    """
    session = google_api_auth()
    return gspread.Client(
        auth=None,
        session=session
    )


def lista_frases(url, orgao):
    com_orgao = [
        f"🤖 O portal com dados públicos {url} do órgão {orgao} parece não estar funcionando. Poderia me ajudar a checar?",
        f"🤖 Hum, parece que o site {url}, mantido pelo órgão {orgao}, está apresentando erro. Poderia dar uma olhadinha?",
        f"🤖 Poxa, tentei acessar {url} e não consegui. Este site é mantido pelo órgão {orgao}. Você pode confirmar isso?",
        f"🤖 Não consigo acessar {url}, e eu sei que ele é mantido pelo órgão {orgao}. Você pode me ajudar a verificar?",
        f"🤖 Sabe o portal {url}, mantido pelo orgão {orgao}? Ele parece estar fora do ar. Você pode confirmar?",
        f"🤖 Parece que {url} está apresentando probleminhas para ser acessado. Alguém pode avisar a(o) {orgao}?",
        f"🤖 Oi, parece que esse site {url} possui problemas de acesso. {orgao} está sabendo disso?",
        f"🤖 Portais da transparência são um direito ao acesso à informação {orgao}, mas parece que {url} está fora do ar.",
        f"🤖 Opa {orgao}, parece que o site {url} não está acessível como deveria. O que está acontecendo?",
        f"🤖 Tentei acessar o site {url} e não consegui. {orgao} está acontecendo algum problema com essa portal de transparência?",
    ]
    return random.choice(com_orgao)


def checar_timelines(twitter_hander, mastodon_handler, url, orgao, limit=10):
    """
    Recupera os [limit] últimos toots da conta do Mastodon.
    Caso a URL não esteja entre as últimas notificadas, é feita a postagem.
    Feature necessária para não floodar a timeline alheia caso um site fique offline por longos períodos de tempo.
    """

    timeline = mastodon_handler.timeline_home(limit)
    urls_postadas = [toot["content"] for toot in timeline]
    contem = any(url in toot for toot in urls_postadas)
    if not contem:
        mastodon_handler.toot(lista_frases(url=url, orgao=orgao))
        twitter_hander.update_status(status=lista_frases(url=url, orgao=orgao))
