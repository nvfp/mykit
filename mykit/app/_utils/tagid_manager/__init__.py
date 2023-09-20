import random


class TagIdManager:

    objs_by_id  = {}  # All components combined
    objs_by_tag = {}  # All components combined

    def get_all_objs_by_id(id:str, /) -> int:
        pass

    def get_obj_by_id(id:str, /) -> int:
        pass

    def get_objs_by_tag(tag:str, /) -> int:
        pass

    @staticmethod
    def register_tagid(id, tags):
        
        ## self.id ensures that we can modify a specific instance without affecting the others
        if id is None:
            self.id = str(_random.randint(0, 100_000))
            while self.id in Button.buttons:
                self.id = str(_random.randint(0, 100_000))
        else:
            self.id = id
            if self.id in Button.buttons:
                raise ValueError(f'The id {repr(id)} is duplicated.')
        
        Button.buttons[self.id] = self

        ## </id>

        ## <tags>

        if type(tags) is str:
            self.tags = [tags]
        elif (type(tags) is list) or (type(tags) is tuple) or (tags is None):
            self.tags = tags
        
        if tags is not None:
            for tag in self.tags:
                if tag in Button.button_tags:
                    Button.button_tags[tag].append(self)
                else:
                    Button.button_tags[tag] = [self]