"""Museums."""
# from datetime import time

# from bod.objects import Link
# from bod.mkrf.objects import Museum as Museum_src
# from bod.objects import Museum as Museum_dst


# class Museum:
#     """Museums."""
#     def __init__(self):
#         self.data = {}

#     def convert_data(self): ...

#     def parse_external_info(self):
#         data: list = self.data.get('externalInfo', None)
#         links = []
#         if data:
#             for item in data:
#                 link = Link(description=item.get('serviceName', None),
#                             url=item.get('url', None))
#                 links.append(link)
#             return links
#         return None

#     def parse_workingSchedule(self):
#         data: dict = self.data.get('workingSchedule', None)
#         if data:
#             result = {}
#             mapping = {
#                 '0': 'Monday',
#                 '1': 'Tuesday',
#                 '2': 'Wednesday',
#                 '3': 'Thursday',
#                 '4': 'Friday',
#                 '5': 'Saturday',
#                 '6': 'Sunday'
#             }
#             for key, value in data.items():
#                 start_time = time.fromisoformat(value['from']).strftime('%H:%M')
#                 end_time = time.fromisoformat(value['to']).strftime('%H:%M')
#                 value = {
#                     'start': start_time,
#                     'end': end_time
#                 }
#                 result.update({mapping.get(key, None): value})
#             return result
#         return None

#     def parse_organization(self):
#         data: dict = self.data.get('organization', None)
#         if data:
#             result = {
#                 'name': data.get('name', None),
#                 'address': {
#                     'street': data.get('address', None).get('street', None),
#                     'comment': data.get('address', None).get('comment', None),
#                     'fullAddress': data.get('address', None).get('fullAddress', None),
#                     'mapPosition': data.get('address', None).get('mapPosition', None)
#                 },
#                 'inn': data.get('inn', None),
#                 'type': data.get('type', None),
#                 'subordination': {
#                     'name': data.get('subordination', None).get('name', None),
#                     'timezone': data.get('subordination', None).get('timezone', None)
#                 },
#                 'socialGroups': []
#             }
#             socialGroups = data.get('socialGroups', None)
#             if socialGroups:
#                 for socialGroup in socialGroups:
#                     ...

#     def parse_tags(self):
#         data: list = self.data.get('tags', None)
#         tags = []
#         if data:
#             for tag in data:
#                 if name := tag.get('name', None):
#                     tags.append(name)

#     def parse_contacts(self):
#         data: dict = self.data.get('contacts', None)
#         if data:
#             result = {
#                 'website': data.get('website', None),
#                 'email': data.get('email', None),
#                 'phones': []
#             }
#             phones = data.get('phones', None)
#             if phones:
#                 for phone in phones:
#                     result['phones'].append({
#                         'type': phone.get('type', None),
#                         'value': phone.get('value', None),
#                         'comment': phone.get('comment', None)
#                     })
#             return result
#         return None

#     def parse_gallery(self):
#         data: list = self.data.get('gallery', None)
#         links = []
#         if data:
#             for item in data:
#                 link = Link(type='image', 
#                             url=item.get('url', None),
#                             description=item.get('title', None))
#                 links.append(link)
#             return links
#         return None

#     def parse_address(self):
#         data: dict = self.data.get('address', None)
#         if data:
#             result = {
#                 'street': data.get('street', None),
#                 'comment': data.get('comment', None),
#                 'fiasSettlementId': data.get('fiasSettlementId', None),
#                 'fiasAreaId': data.get('fiasAreaId', None),
#                 'fiasRegionId': data.get('fiasRegionId', None),
#                 'fullAddress': data.get('fullAddress', None),
#                 'mapPosition': data.get('mapPosition', None)
#             }
#             for key, value in result.items():
#                 if not value:
#                     del result[key]
#         return result

#     def parse_category(self):
#         data = self.data.get('category', None)
#         if data:
#             return data.get('name', None)
#         return None

#     def parse_link(self):
#         data = self.data.get('links', None)
#         links = []
#         for item in data:
#             link = Link(type='link',
#                         url=item.get('url', None),
#                         description=item.get('serviceName', None))
#             links.append(link)
#         return links

#     def parse_external_ids(self):
#         data = self.data.get('externalIds', None)
#         external_ids = []
#         if data:
#             for key, value in data.items():
#                 external_id = {'name': key,
#                                'value': value}
#                 external_ids.append(external_id)
#         return external_ids if external_ids else None

#     def parse_mapPosition(data: dict) -> dict:
#         _type = data.get('type', None)
#         _coordinates = data.get('coordinates', None)
#         if _type == "Point":
#             coordinates = Point(_coordinates)
#         elif _type == "":
#             coordinates = None
#         elif _type == "":
#             coordinates = None
#         if (_type is not None and coordinates is not None):
#             return {
#                 'type': _type,
#                 'coordinates': coordinates,
#                 'centroid': None
#             }
#         return None


# def parse_museum(data: dict) -> Museum_dst:
#     """Parse a data from given dict."""

#     obj = Museum_src(**data)

#     return obj
