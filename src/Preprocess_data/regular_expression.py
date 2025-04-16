import re


def hide_phone_numbers(text):
    # 通过正则表达式隐藏电话号码中间的数字
    return re.sub(r'\d{3}-\d{4}-(\d{4})', r'***-****-\1', text)

def hide_email_addresses(text):
    # 通过正则表达式隐藏邮箱用户名部分
    return re.sub(r'(\w+)(@\w+\.\w+)', r'***\2', text)

def hide_id_numbers(text):
    # 通过正则表达式隐藏身份证号码的部分数字
    return re.sub(r'\d{6}(?:19|20)\d{2}\d{2}\d{2}\d{2}\d{1}', r'**************\\d', text)

def hide_card_numbers(sentence):
    # 正则表达式模式，用于匹配银行卡号（16位数字）
    card_number_pattern = r'\d{16}'

    # 使用正则表达式查找句子中的银行卡号
    card_numbers = re.findall(card_number_pattern, sentence)

    # 将句子中的银行卡号替换为星号(*)，保留首尾各4位数字
    for card_number in card_numbers:
        masked_card_number = card_number[:4] + '*' * 8 + card_number[-4:]
        sentence = sentence.replace(card_number, masked_card_number)

    return sentence


def hide_ip_addresses(sentence):
    # 正则表达式模式，用于匹配IPv4地址
    ip_address_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

    # 使用正则表达式查找句子中的所有IP地址
    ip_addresses = re.findall(ip_address_pattern, sentence)

    # 将句子中的IP地址替换为星号(*)
    for ip_address in ip_addresses:
        masked_ip_address = '*' * len(ip_address)
        sentence = sentence.replace(ip_address, masked_ip_address)

    return sentence