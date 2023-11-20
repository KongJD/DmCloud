import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re

# url = 'https://doi.org/10.1128/jcm.00853-10'
url = 'https://journals.asm.org/doi/10.1128/jcm.00853-10'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    # "cookie": "__cf_bm=oPzG3DU_mZbLeI.LsPZtX5aV1CSW0MVKgaKA1.2a.Mw-1697607578-0-AfROui+gVfYg+vCzHCYEkjwSDtHLvA2uYlVZGQGuPXAxgMB2mb2kfpt4HcBAbLnlsOdnEVEyns/htqi2V7SIX1ITrRXTQXcMy3IKqbCl8Mlr; EUID=dd9c4cdb-f419-4946-b8a8-bc6b9b7f374a; sd_session_id=b39e6b80244ef84a806b9be3af2e3a107585gxrqa; acw=b39e6b80244ef84a806b9be3af2e3a107585gxrqa%7C%24%7C3B3C2354EEEC14CE07C898E40E17F044F0FCB7D673FF81F0582A3E81AB4DA886AF0F7E146B897B792670FF0E500B11BD1B4DD98BA15AD0CA3FBA44D1BD4E4F2EB0469A67597464825D387A21AFA2E514; id_ab=AEG; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; cf_clearance=58aKAjqLOjfpLW.QlJBlt.sQIxWSI847AhTunocyuKQ-1697607581-0-1-326a77d6.56149f78.656b2836-0.2.1697607581; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=179643557%7CMCIDTS%7C19649%7CMCMID%7C89959368917805931974581088588042637265%7CMCAAMLH-1698212381%7C11%7CMCAAMB-1698212381%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1697614781s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-1660478464%7CvVersion%7C5.5.0; mboxes=%7B%22header-sign-in%22%3A%7B%22variation%22%3A%22%232%22%2C%22enabled%22%3Atrue%7D%7D; MIAMISESSION=b8086cf4-9b59-488a-8829-2b164f51ba17:3875061967; mbox=session%23121823e547f040058003f47f096bae6c%231697611028%7CPC%23121823e547f040058003f47f096bae6c.34_0%231760853968; s_pers=%20c19%3Dsd%253Aproduct%253Ajournal%253Aarticle%7C1697610968546%3B%20v68%3D1697609167353%7C1697610968551%3B%20v8%3D1697609168558%7C1792217168558%3B%20v8_s%3DFirst%2520Visit%7C1697610968558%3B; s_sess=%20s_cpc%3D0%3B%20s_sq%3D%3B%20s_ppvl%3Dsd%25253Aproduct%25253Ajournal%25253Aarticle%252C13%252C7%252C923%252C1920%252C923%252C1920%252C1080%252C1%252CP%3B%20e41%3D1%3B%20s_cc%3Dtrue%3B%20s_ppv%3Dsd%25253Aproduct%25253Ajournal%25253Aarticle%252C13%252C3%252C923%252C1920%252C205%252C1920%252C1080%252C1%252CP%3B",
}
res = requests.get(url, headers=headers)
print(res.text)

soup = BeautifulSoup(res.text, 'html.parser')
# pattern =re.compile(r"articleName\s*:\s*'([^']+)'")
#
# script = soup.find('script', text=pattern)
#
# data_str = pattern.search(script.text).group(1)
#
# print(data_str)
tile= soup.find("div", {'class': "metadata_title"})
print(tile.text)


class ElasticCountryExtraView(GenericAPIView):

    def get(self, request):
        http_request = HttpRequest()
        http_request.method = 'GET'
        http_request.GET = QueryDict(request.META['QUERY_STRING'])
        view_ = ElasticCountrySourceView.as_view(actions={"get": "list"})
        resposne_ = view_(http_request)
        data_ = resposne_.data['results']
        if not data_:
            return Response([])

        unique_values = {}
        attributes = {
            "country": [],
            "source": [],
        }
        for item in data_:
            for attr, value in attributes.items():
                if item[attr] != None:
                    if item[attr].strip():
                        value.append(item[attr].strip())
                    # value.extend([m for m in item[attr].strip().split(";") if m])

        unique_values["country"] = dict(Counter(attributes['country']))
        unique_values["source"] = "\n\n".join(list(set(attributes["source"])))

        return Response(unique_values, status=status.HTTP_200_OK)

class ElasticExtra1View(GenericAPIView):

    def get(self, request):
        http_request = HttpRequest()
        http_request.method = 'GET'
        http_request.GET = QueryDict(request.META['QUERY_STRING'])
        view_ = ElasticExtraOtherView.as_view(actions={"get": "list"})
        resposne_ = view_(http_request)
        data_ = resposne_.data['results']
        if not data_:
            return Response([])
        attributes = {
            # "species": [],
            "colony_size": [],
            "hemolysis": [],
            "antibiotic_resistance": [],
            "sensitivity_to_antibiotics": [],
            "nutrition_type": [],
            "gc_content": []
        }
        exclude = ["colony_size", "gc_content"]
        for item in data_:
            for attr, value in attributes.items():
                if item[attr] != None and item[attr].strip():
                    if attr in exclude:
                        value.append(round(np.mean([float(m) for m in re.findall(r'\d+\.?\d*e?\d*?',
                                                                                 item[attr].strip())]), 2))
                    else:
                        for ms in item[attr].strip().split(","):
                            ms = ms.strip()
                            if ms:
                                if "and" in ms:
                                    mst = ms.split("and")
                                    for gg in mst:
                                        if gg.strip():
                                            value.append(gg.strip())
                                else:
                                    value.append(ms)

        all = {attr: dict(Counter(value)) for attr, value in attributes.items()}

        return Response(all, status=status.HTTP_200_OK)


class ElasticFullSpeciesExtraView(GenericAPIView):
    pagination_class = MyPageNumberPageination
    serializer_class = SpeciesTypeExtraSerilzer

    def get(self, request):
        http_request = HttpRequest()
        http_request.method = 'GET'
        http_request.GET = QueryDict(request.META['QUERY_STRING'])
        view_ = ElasticFullSpeciesView.as_view(actions={"get": "list"})
        resposne_ = view_(http_request)
        data_ = resposne_.data['results']

        result = {}
        for item in data_:
            key = (item['species'], item['species_cn'], item['status'])
            if key in result:
                result[key]['count'] += item['count']
            else:
                result[key] = item
        data_list = list(result.values())
        page = self.paginate_queryset(data_list)
        if page is not None:
            ser_data = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser_data.data)
        ser_data = self.get_serializer(data_list, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)
