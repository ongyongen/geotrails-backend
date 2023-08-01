
def create_geocaches_filter_criteria(
        geocache_types, 
        container_types, 
        difficulty, 
        terrain, 
        planning_areas,
        geocache_code
):
    
    criteria = {}
    if geocache_types != []:
        criteria["geocache_type"] = { "$in" : geocache_types }
    if container_types != []:
        criteria["container_type"] = { "$in" : container_types }
    if difficulty != "":
        criteria["difficulty"] = { "$lte" : difficulty }
    if terrain != "":
        criteria["terrain"] = { "$lte" : terrain }
    if planning_areas != []:
        criteria["planning_area"] = { "$in" : planning_areas }
    if geocache_code != None:
        code_regex =  "^" + geocache_code 
        criteria["cache_code"] = {"$regex": code_regex, "$options": 'i'}

    return criteria if criteria != {} else {}
    