import random as _random
from typing import (
    Callable as _Callable,
    Dict as _Dict,
    List as _List,
    Literal as _Literal,
    Optional as _Optional,
    Tuple as _Tuple,
    Union as _Union
)

from mykit.app.utils.types import Component as _Component


class TagIdManager:  # TODO: potentially soon this class could be renamed to just 'TagId' if no conflicts occur

    ## Note that a single ID here can now hold multiple components.
    ## This is because the ID is only unique under each component but can be shared overall, to make it more flexible.
    objs_by_id:  _Dict[str, _List[_Component]] = {}  # All components combined
    objs_by_tag: _Dict[str, _List[_Component]] = {}  # All components combined

    @staticmethod
    def get_all_objs_by_id(id:str, /) -> _List[_Component]:
        """
        Get all objects that match the given `id`.

        ## Exceptions
        - `ValueError`: If the given `id` matches no objects.

        ## Docs
        - Note, the returned list is not a copied list, so please be careful when doing something to it.
        """
        if id not in TagIdManager.objs_by_id: raise ValueError(f"There are no objects with id {repr(id)}.")
        return TagIdManager.objs_by_id[id]

    @staticmethod
    def get_obj_by_id(id:str, /) -> _Component:
        """
        Get object with given `id`, believing there is only one object with that ID.

        ## Exceptions
        - `ValueError`: If the given `id` matches no objects.
        - `AssertionError`: If more than one object shares the same `id`.
        """
        if id not in TagIdManager.objs_by_id: raise ValueError(f"There are no objects with id {repr(id)}.")
        objs = TagIdManager.objs_by_id[id]
        if len(objs) != 1: raise AssertionError(f"Multiple objects have the same ID {repr(id)}, when there should be only one.")
        return objs[0]

    @staticmethod
    def get_objs_by_tag(tag:str, /) -> _List[_Component]:
        """
        Get all objects that match the given `tag`.

        ## Exceptions
        - `ValueError`: If the given `tag` matches no objects.

        ## Docs
        - Note, the returned list is not a copied list, so please be careful when doing something to it.
        """
        if tag not in TagIdManager.objs_by_tag: raise ValueError(f"There are no objects with tag {repr(tag)}.")
        return TagIdManager.objs_by_tag[tag]

    @staticmethod
    def _register_tagid(component, runtime, id, tags):  # For internal use only

        ## ID

        if id is None:
            the_id = str(_random.randint(0, 100_000))
            while the_id in runtime.instances:
                the_id = str(_random.randint(0, 100_000))
        else:
            the_id = id
            if the_id in runtime.instances:
                raise ValueError(f'The ID {repr(id)} is duplicated.')

        component.id = the_id  # Assign the ID to the component.
        runtime.instances[the_id] = component  # Register the unique ID in the component ID pool
        if the_id in TagIdManager.objs_by_id:  # Register the ID in the TagIdManager ID pool
            TagIdManager.objs_by_id[the_id].append(component)
        else:
            TagIdManager.objs_by_id[the_id] = [component]

        ## Tags

        if type(tags) is str:
            component.tags = [tags]
        elif (type(tags) is list) or (type(tags) is tuple) or (tags is None):
            component.tags = tags

        if component.tags is not None:
            for tag in component.tags:

                ## Local tags pool (component)
                if tag in runtime.groups: runtime.groups[tag].append(component)
                else: runtime.groups[tag] = [component]

                ## Global tags pool (TagIdManager)
                if tag in TagIdManager.objs_by_tag: TagIdManager.objs_by_tag[tag].append(component)
                else: TagIdManager.objs_by_tag[tag] = [component]
