from testo2 import PROXY
import requests

cookies = {
    '_gid': 'GA1.2.805589226.1724999673',
    '_ga_L5S0QVWQE6': 'GS1.1.1724999673.1.0.1724999673.60.0.0',
    'corp_locale': 'en-us',
    '__zlcmid': '1NVmyxR7JKtTrNR',
    'sgID': '5b8c46bc-99b0-4cc1-ac1f-d012d4f56f5d',
    'bm_mi': '53C1D3AC8F03282AFE3773A1E79DA3F6~YAAQrG9kX9kfJZeRAQAACwElohihwAzCdh8ymObSLY/etMCYkMK6K5f1yP7ykkvqfik7kwweb6X5lWedfxI9HVccR1PFZ35AZ7QO9dYaqKs0zCaJA9JckDuqGKKTjNF3C/m4TeychUIMQjBCs81tMEejwADJX+xip8PjSCDEGRAldQkHM8L5WZldCNV036hfQv9tWe/mCIQBDfwUIzEuWTHHFqCyDHxSQOanJWezbDmo02uQ7+cpF4IXjlhZIp+v6R9lW+03BNbvG0qzcBBMDVuD73ftt+3Rfii4W3eJp2VwvoX+66Yp1D23wMrdo7E=~1',
    '_abck': '764D9944670036538AD650E9163766F4~0~YAAQrG9kX94fJZeRAQAAewMlogwWRL2dZHtOYK3SIx6ktvQAHoPymMBSS6Y7MlKDAIxJGPeP6Hk35+l0geMZzu0SaWj1xm8ituPmxmmQFLkbNgVPlLjFO59LzpfiOfTDAQ9a/Nc9I+GgRYNyskVJ9GUz/YAPuHKRQwQvY0HAf2Q4k5TcfARmvsf18LaeXry8DTDNHgebZ/HJ1hzfgnL48UdYaTzbFSgQ7QxaQUcAUOe1532FKLOD0ab6HKxOCii3FCvXxduDAqWnhmNCEW+kEwttySVHMf0Rk1nrohFIRiPxXuyTrl/HnADcULcmVi6S3Ph1Gz3gwIOerzcK0pC+l5qENlBvHHRexc6mKGoKsSgBeub2JJ/dJp4tPwGlPFFw7MOUnoYlHI/hXIGhsoFpVtWXOrY1W0GpeBkD~-1~||0||~-1',
    '_gcl_au': '1.1.1987514933.1725002220',
    'ak_bmsc': '5DD3011E321E996F44463380BD83E24F~000000000000000000000000000000~YAAQrG9kX+AfJZeRAQAANwUlohjW4yvmsIqXRD3l1LXRH+CWFmluNe6gV3SosuUsFgVMkQMxMtkue7iZkgfBqjgsvlHvedRe4yJPkQ+xqdJBpXsiXNZECSR6FKzE8BuQ80a1Rr6pTbEWQ4W945OXWWBLVSrFqWz5iN9TQPWrUWoU5Q4sEVkKSpKFPMMMF39jUWqwHWe1lDkRcIr7SxHzQ0+xxizLzfLPND0uMLv/qqNaLWFvf1cL1t0RxeQcYhNOK4VR9mLLaAbq2KuBxX/8caFr/Bnjye2li8SYy1H9/jb+0Iuhay7sAcVUaqQ4Ohghm+CiNdxB6T6mPYSA0koku10MetzYfvjPfclMln83fX6gif3UY0njng8vX1YqOO6fZpS2RB5NFLnPLMKQLdjkWu9n7eMebHypYKT7A0RWMh+5ARgcnT/CTu9D2WPu5R2Yvt7qDbzQ3g/OzyhfHI2ISz/3dLqRT+5iZK9PoeFfiJMj',
    'FPAU': '1.1.1987514933.1725002220',
    '_pk_ref.1.fd33': '%5B%22%22%2C%22%22%2C1725002222%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D',
    '_pk_id.1.fd33': '13e4c4d9837e9cfb.1725002222.',
    '_pk_ses.1.fd33': '1',
    'locale': 'en-us',
    'sw_reg_params': 'action%3Dwebsite_performance%26domain%3Ddropship.io',
    '_vis_opt_s': '1%7C',
    '_vis_opt_test_cookie': '1',
    '_vwo_uuid': 'J7AE6B959E05499398C56E85304F905D9',
    '_vwo_ds': '3%241725002241%3A24.21154608%3A%3A',
    'fsrndidpro': 'false',
    '_tt_enable_cookie': '1',
    '_ttp': 'vW-majqhiB74JTI2KZbzMU1IcAp',
    '_fbp': 'fb.1.1725002242374.37692368327991151',
    '_clck': '2ks3yv%7C2%7Cfor%7C0%7C1703',
    '.DEVICETOKEN.SIMILARWEB.COM': '8aK2X32ps7IPhvDNPR2l70RMN0MaSQ8k',
    '.SGTOKEN.SIMILARWEB.COM': 'EMGY7lVOeD5XYKvb9UQKY5A3vciol8vO3Nxf9RU_40bdqJ4SpfSTmbRGbxgDnUJ-whiU6didOSmLiw_3QM1Fdt0yayWq-RjP0rlYAkDShvx9rQPGQyJ4oMgMtWBItY3FIggVGoNfVPU2VXiOxhW3e3_jeX0kLrWJuCXPqfxa1Q_sYL72X0-PkQc1PbYgo2FKYyGLX27GGQyocRK6dJUeBBS8RWtCBNQRvF0lvU5LpYBRaXA5hIU0rqo-P1bL6GDGP3NeHS0TYfbTejIBywYSfeEL_dc4kE504PUbj1VRXPtnIzS8bwGFgn8EC_Fy9NxIt2feVdz_UzOmOg3z6O19MB9K1K9sOKTRrRWft0JqzJ0NGLAbu3ZQUhfAWxcipXHFRJtV92QdzGtJ8ce-Uuon8RcWr4qAfy7i_pF4NtI1YBRHhu22FEnX1heMHn6S4yob5eEIPkqh9mQzuInisJtRSv-eFrsocu2ez_XnQgtutSliw18Mf7WmkDkp862nwSZWzVqWhXXruDPRcQpVVvoc_Q',
    '_sw_pin': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNDY2OTgyNSIsInRpZCI6IjEwMDAwMDM1IiwicHN0IjoiMCIsInFuIjoiLlNHVE9LRU4uU0lNSUxBUldFQi5DT00iLCJxaCI6ImVkN2I5NmJiZGExZGU0MmQ0MjhkNTgzYzMwOTFiYWQwIiwibmJmIjoxNzI1MDAyMjUzLCJleHAiOjE3MjUwMDU4NTMsImlhdCI6MTcyNTAwMjI1MywiaXNzIjoiaHR0cHM6Ly9zZWN1cmUuc2ltaWxhcndlYi5jb20ifQ.HDBEIT6QgsJp2o8gN5Ei8kh7psezyExI9vhSehHV6PDVLP0i38dCwBXlVfIBepPW7L4h9mfUTLz2soGgAXrBAGyladkshDtSFNgEcKpCb2i9yiNWdTI8HKS9tDAG77dihdwsaRs3G4JcPL25sJclSDPPaS3KtQuNkfya0Ixo8mEO_-7BqFbO5myEMJZvqN3GgNbSx66MaFZBBzLDctkKNnHtC45EqKOv6h72Svm2TJAuea9qPaqxzFnLSmvOEl3XkV-CFpZ2Vn1Fr5YzKPVJwduVEBw5mLzWr78VzdGj0jts5Z01n_Fg1Hjr6emY7ziBeakjbdl9Kl45Z6bcEOuBaw',
    '_sw_pin_ps': '0',
    'RESET_PRO_CACHE': 'False',
    '_BEAMER_USER_ID_zBwGJEbQ32550': '66f34b79-977c-4374-80a6-87296e68d15e',
    '_BEAMER_FIRST_VISIT_zBwGJEbQ32550': '2024-02-20T08:29:13.707Z',
    '__q_state_9u7uiM39FyWVMWQF': 'eyJ1dWlkIjoiYWFiZWM1MGUtODg5ZC00ZDEwLWJiNzYtNjhjMGE1YjFlNzFiIiwiY29va2llRG9tYWluIjoic2ltaWxhcndlYi5jb20iLCJhY3RpdmVTZXNzaW9uSWQiOm51bGwsInNjcmlwdElkIjoiMTM5MDY1ODI5NTA0NjAyMjMyNyIsIm1lc3NlbmdlckV4cGFuZGVkIjpmYWxzZSwicHJvbXB0RGlzbWlzc2VkIjpmYWxzZSwic3RhdGVCeVNjcmlwdElkIjp7IjE0NjY5MTA2ODk4OTY2OTQ5MzEiOnsiZGlzbWlzc2VkIjpmYWxzZSwic2Vzc2lvbklkIjpudWxsfSwiMTM5MDY1ODI5NTA0NjAyMjMyNyI6eyJkaXNtaXNzZWQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGx9fSwiY29udmVyc2F0aW9uSWQiOiIxNDcyNDE1Njk3MjMyNzc0MjczIn0=',
    '_BEAMER_LAST_UPDATE_zBwGJEbQ32550': '1725002390659',
    'bm_sz': '06C2928BAF7BF709455C558C265F5CD3~YAAQn29kX8f13nuRAQAAPKg6ohhBR4EPDGWx1p1mqu9MA/J7ppOkZKDX7+ezYXtIsYvRXxAowplziH/KT0X6qsJSS/quNn2wzxwKanbNoK59PYvzaJm44jvAgqmI1f1M6rxHLINWoq4dPsAg3Jr+3qvFzpRAh+ZDOF903BePVEmd9k+ZiieRJ2lZ8rW7CIqygv4fTlQvuf975i0EqLLRxx0y539h3CM2eDeNjE6/C+u3LU4JFdYaiEiu3Jsvjn8X3gfJiWYN1qR+Vc21deR3T8sD4SIF9moMO5UVoQD43lO5Vx9xBmVxq0m3XyvFD4XIu/CSmcFE71ZVk/E9Vrp8kLg/LdBC7Mpt3CkVAxI/2cN1t0UvJTJwaAKEUGUHDM/YwxBB5Z7ge90gZqgxAKJKrx9RVV4NkrZmjbN6VQkm2jCk41iXJ0l9ZZgWTe45zKmp535akA==~3228738~3227960',
    '_ga_V5DSP51YD': 'GS1.1.1725002255.1.1.1725003645.0.0.0',
    '_ga': 'GA1.1.189342388.1724999673',
    '_ga_V5DSP51YD0': 'GS1.1.1725002220.1.1.1725003645.0.0.1690765580',
    '_uetsid': 'e66a4140669f11ef836afb08a539bd6f',
    '_uetvid': 'e66a5970669f11efa9a5839b0e98020a',
    '_ga_JKZGLE7YPK': 'GS1.2.1725002264.1.1.1725003645.0.0.0',
    'bm_sv': '2C15D4BEC0AF05F33FBF28C94B51AB9B~YAAQn29kX/H13nuRAQAAkcM6ohgY134Chw1mvGvoJsVhKPyEOhJrXNAhP+7po3kCbrQdmZyrtyGDiJmDaLCJbXJEdTQ/Ka8pAdv8ZaxDCPePOdQ96WvYb3S9naLOdwpO3TRD36DM3o2+pOnmA04Tw3RmoAdLjV7PQYneBsKLwHm/qSIY0Cdxzu0DpANT2KCXFDzBnV83VV7q2IAKBe0O5eXHgATbrVeTpWoxEATfSfX+pr3nAD5l9rCehrTju0ijQ63RJwM=~1',
    '_clsk': '1im4zq5%7C1725005015510%7C4%7C1%7Ci.clarity.ms%2Fcollect',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,uk;q=0.8',
    'cache-control': 'no-cache',
    # 'cookie': '_gid=GA1.2.805589226.1724999673; _ga_L5S0QVWQE6=GS1.1.1724999673.1.0.1724999673.60.0.0; corp_locale=en-us; __zlcmid=1NVmyxR7JKtTrNR; sgID=5b8c46bc-99b0-4cc1-ac1f-d012d4f56f5d; bm_mi=53C1D3AC8F03282AFE3773A1E79DA3F6~YAAQrG9kX9kfJZeRAQAACwElohihwAzCdh8ymObSLY/etMCYkMK6K5f1yP7ykkvqfik7kwweb6X5lWedfxI9HVccR1PFZ35AZ7QO9dYaqKs0zCaJA9JckDuqGKKTjNF3C/m4TeychUIMQjBCs81tMEejwADJX+xip8PjSCDEGRAldQkHM8L5WZldCNV036hfQv9tWe/mCIQBDfwUIzEuWTHHFqCyDHxSQOanJWezbDmo02uQ7+cpF4IXjlhZIp+v6R9lW+03BNbvG0qzcBBMDVuD73ftt+3Rfii4W3eJp2VwvoX+66Yp1D23wMrdo7E=~1; _abck=764D9944670036538AD650E9163766F4~0~YAAQrG9kX94fJZeRAQAAewMlogwWRL2dZHtOYK3SIx6ktvQAHoPymMBSS6Y7MlKDAIxJGPeP6Hk35+l0geMZzu0SaWj1xm8ituPmxmmQFLkbNgVPlLjFO59LzpfiOfTDAQ9a/Nc9I+GgRYNyskVJ9GUz/YAPuHKRQwQvY0HAf2Q4k5TcfARmvsf18LaeXry8DTDNHgebZ/HJ1hzfgnL48UdYaTzbFSgQ7QxaQUcAUOe1532FKLOD0ab6HKxOCii3FCvXxduDAqWnhmNCEW+kEwttySVHMf0Rk1nrohFIRiPxXuyTrl/HnADcULcmVi6S3Ph1Gz3gwIOerzcK0pC+l5qENlBvHHRexc6mKGoKsSgBeub2JJ/dJp4tPwGlPFFw7MOUnoYlHI/hXIGhsoFpVtWXOrY1W0GpeBkD~-1~||0||~-1; _gcl_au=1.1.1987514933.1725002220; ak_bmsc=5DD3011E321E996F44463380BD83E24F~000000000000000000000000000000~YAAQrG9kX+AfJZeRAQAANwUlohjW4yvmsIqXRD3l1LXRH+CWFmluNe6gV3SosuUsFgVMkQMxMtkue7iZkgfBqjgsvlHvedRe4yJPkQ+xqdJBpXsiXNZECSR6FKzE8BuQ80a1Rr6pTbEWQ4W945OXWWBLVSrFqWz5iN9TQPWrUWoU5Q4sEVkKSpKFPMMMF39jUWqwHWe1lDkRcIr7SxHzQ0+xxizLzfLPND0uMLv/qqNaLWFvf1cL1t0RxeQcYhNOK4VR9mLLaAbq2KuBxX/8caFr/Bnjye2li8SYy1H9/jb+0Iuhay7sAcVUaqQ4Ohghm+CiNdxB6T6mPYSA0koku10MetzYfvjPfclMln83fX6gif3UY0njng8vX1YqOO6fZpS2RB5NFLnPLMKQLdjkWu9n7eMebHypYKT7A0RWMh+5ARgcnT/CTu9D2WPu5R2Yvt7qDbzQ3g/OzyhfHI2ISz/3dLqRT+5iZK9PoeFfiJMj; FPAU=1.1.1987514933.1725002220; _pk_ref.1.fd33=%5B%22%22%2C%22%22%2C1725002222%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_id.1.fd33=13e4c4d9837e9cfb.1725002222.; _pk_ses.1.fd33=1; locale=en-us; sw_reg_params=action%3Dwebsite_performance%26domain%3Ddropship.io; _vis_opt_s=1%7C; _vis_opt_test_cookie=1; _vwo_uuid=J7AE6B959E05499398C56E85304F905D9; _vwo_ds=3%241725002241%3A24.21154608%3A%3A; fsrndidpro=false; _tt_enable_cookie=1; _ttp=vW-majqhiB74JTI2KZbzMU1IcAp; _fbp=fb.1.1725002242374.37692368327991151; _clck=2ks3yv%7C2%7Cfor%7C0%7C1703; .DEVICETOKEN.SIMILARWEB.COM=8aK2X32ps7IPhvDNPR2l70RMN0MaSQ8k; .SGTOKEN.SIMILARWEB.COM=EMGY7lVOeD5XYKvb9UQKY5A3vciol8vO3Nxf9RU_40bdqJ4SpfSTmbRGbxgDnUJ-whiU6didOSmLiw_3QM1Fdt0yayWq-RjP0rlYAkDShvx9rQPGQyJ4oMgMtWBItY3FIggVGoNfVPU2VXiOxhW3e3_jeX0kLrWJuCXPqfxa1Q_sYL72X0-PkQc1PbYgo2FKYyGLX27GGQyocRK6dJUeBBS8RWtCBNQRvF0lvU5LpYBRaXA5hIU0rqo-P1bL6GDGP3NeHS0TYfbTejIBywYSfeEL_dc4kE504PUbj1VRXPtnIzS8bwGFgn8EC_Fy9NxIt2feVdz_UzOmOg3z6O19MB9K1K9sOKTRrRWft0JqzJ0NGLAbu3ZQUhfAWxcipXHFRJtV92QdzGtJ8ce-Uuon8RcWr4qAfy7i_pF4NtI1YBRHhu22FEnX1heMHn6S4yob5eEIPkqh9mQzuInisJtRSv-eFrsocu2ez_XnQgtutSliw18Mf7WmkDkp862nwSZWzVqWhXXruDPRcQpVVvoc_Q; _sw_pin=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNDY2OTgyNSIsInRpZCI6IjEwMDAwMDM1IiwicHN0IjoiMCIsInFuIjoiLlNHVE9LRU4uU0lNSUxBUldFQi5DT00iLCJxaCI6ImVkN2I5NmJiZGExZGU0MmQ0MjhkNTgzYzMwOTFiYWQwIiwibmJmIjoxNzI1MDAyMjUzLCJleHAiOjE3MjUwMDU4NTMsImlhdCI6MTcyNTAwMjI1MywiaXNzIjoiaHR0cHM6Ly9zZWN1cmUuc2ltaWxhcndlYi5jb20ifQ.HDBEIT6QgsJp2o8gN5Ei8kh7psezyExI9vhSehHV6PDVLP0i38dCwBXlVfIBepPW7L4h9mfUTLz2soGgAXrBAGyladkshDtSFNgEcKpCb2i9yiNWdTI8HKS9tDAG77dihdwsaRs3G4JcPL25sJclSDPPaS3KtQuNkfya0Ixo8mEO_-7BqFbO5myEMJZvqN3GgNbSx66MaFZBBzLDctkKNnHtC45EqKOv6h72Svm2TJAuea9qPaqxzFnLSmvOEl3XkV-CFpZ2Vn1Fr5YzKPVJwduVEBw5mLzWr78VzdGj0jts5Z01n_Fg1Hjr6emY7ziBeakjbdl9Kl45Z6bcEOuBaw; _sw_pin_ps=0; RESET_PRO_CACHE=False; _BEAMER_USER_ID_zBwGJEbQ32550=66f34b79-977c-4374-80a6-87296e68d15e; _BEAMER_FIRST_VISIT_zBwGJEbQ32550=2024-02-20T08:29:13.707Z; __q_state_9u7uiM39FyWVMWQF=eyJ1dWlkIjoiYWFiZWM1MGUtODg5ZC00ZDEwLWJiNzYtNjhjMGE1YjFlNzFiIiwiY29va2llRG9tYWluIjoic2ltaWxhcndlYi5jb20iLCJhY3RpdmVTZXNzaW9uSWQiOm51bGwsInNjcmlwdElkIjoiMTM5MDY1ODI5NTA0NjAyMjMyNyIsIm1lc3NlbmdlckV4cGFuZGVkIjpmYWxzZSwicHJvbXB0RGlzbWlzc2VkIjpmYWxzZSwic3RhdGVCeVNjcmlwdElkIjp7IjE0NjY5MTA2ODk4OTY2OTQ5MzEiOnsiZGlzbWlzc2VkIjpmYWxzZSwic2Vzc2lvbklkIjpudWxsfSwiMTM5MDY1ODI5NTA0NjAyMjMyNyI6eyJkaXNtaXNzZWQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGx9fSwiY29udmVyc2F0aW9uSWQiOiIxNDcyNDE1Njk3MjMyNzc0MjczIn0=; _BEAMER_LAST_UPDATE_zBwGJEbQ32550=1725002390659; bm_sz=06C2928BAF7BF709455C558C265F5CD3~YAAQn29kX8f13nuRAQAAPKg6ohhBR4EPDGWx1p1mqu9MA/J7ppOkZKDX7+ezYXtIsYvRXxAowplziH/KT0X6qsJSS/quNn2wzxwKanbNoK59PYvzaJm44jvAgqmI1f1M6rxHLINWoq4dPsAg3Jr+3qvFzpRAh+ZDOF903BePVEmd9k+ZiieRJ2lZ8rW7CIqygv4fTlQvuf975i0EqLLRxx0y539h3CM2eDeNjE6/C+u3LU4JFdYaiEiu3Jsvjn8X3gfJiWYN1qR+Vc21deR3T8sD4SIF9moMO5UVoQD43lO5Vx9xBmVxq0m3XyvFD4XIu/CSmcFE71ZVk/E9Vrp8kLg/LdBC7Mpt3CkVAxI/2cN1t0UvJTJwaAKEUGUHDM/YwxBB5Z7ge90gZqgxAKJKrx9RVV4NkrZmjbN6VQkm2jCk41iXJ0l9ZZgWTe45zKmp535akA==~3228738~3227960; _ga_V5DSP51YD=GS1.1.1725002255.1.1.1725003645.0.0.0; _ga=GA1.1.189342388.1724999673; _ga_V5DSP51YD0=GS1.1.1725002220.1.1.1725003645.0.0.1690765580; _uetsid=e66a4140669f11ef836afb08a539bd6f; _uetvid=e66a5970669f11efa9a5839b0e98020a; _ga_JKZGLE7YPK=GS1.2.1725002264.1.1.1725003645.0.0.0; bm_sv=2C15D4BEC0AF05F33FBF28C94B51AB9B~YAAQn29kX/H13nuRAQAAkcM6ohgY134Chw1mvGvoJsVhKPyEOhJrXNAhP+7po3kCbrQdmZyrtyGDiJmDaLCJbXJEdTQ/Ka8pAdv8ZaxDCPePOdQ96WvYb3S9naLOdwpO3TRD36DM3o2+pOnmA04Tw3RmoAdLjV7PQYneBsKLwHm/qSIY0Cdxzu0DpANT2KCXFDzBnV83VV7q2IAKBe0O5eXHgATbrVeTpWoxEATfSfX+pr3nAD5l9rCehrTju0ijQ63RJwM=~1; _clsk=1im4zq5%7C1725005015510%7C4%7C1%7Ci.clarity.ms%2Fcollect',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

params = {
    'domain': 'brushhour.co',
}

response = requests.get('https://data.similarweb.com/api/v1/data', params=params,
                        # cookies=cookies,
                        headers=headers)
print(response.content)

import time
from playwright.sync_api import sync_playwright

scriptString = """  
navigator.webdriver = false  
Object.defineProperty(navigator, 'webdriver', {  
get: () => false  
})  
"""


def add_stealth(page):
    page.add_init_script(scriptString)
    return True
 #"bendover:BGWBZRO-1TBG9O0-RA2SHGQ-9CSG6E4-J7QI9QB-OPGMX8P-B9ECWBX@usa.rotating.proxyrack.net:9000"
proxies = {
        "server": "usa.rotating.proxyrack.net:9000",
        'username': 'bendover',
        "password": 'BGWBZRO-1TBG9O0-RA2SHGQ-9CSG6E4-J7QI9QB-OPGMX8P-B9ECWBX',
    }
def render_page(link, wait_for=None, sleep=1):
    all_requests = []

    for try_count in range(2):
        try:

            with sync_playwright() as p:
                browser = p.chromium.launch(proxy=proxies, headless=False)
                context = browser.new_context()
                context.set_extra_http_headers({
                    "Accept": "application/json"
                })
                page = context.new_page()
                add_stealth(page)
                page.goto("https://similarweb.com/", wait_until='load', referer='https://similarweb.com/')
                page.goto(link, wait_until='load', referer='https://similarweb.com/')
                if wait_for:
                    for try_ in range(2):
                        if wait_for not in page.content():
                            time.sleep(sleep // 2)
                            continue
                content = page.content()
                if not content:
                    browser.close()
                    continue
                browser.close()

            return content
        except Exception as e:
            print(e)
            continue


if __name__ == '__main__':
    url = 'https://data.similarweb.com/api/v1/data?domain=brushhour.co'
    render_page(url)