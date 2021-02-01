from kentik_api.public.device_label import DeviceLabel, DeviceItem
from kentik_api.public.types import ID


def test_regular_constructor_success() -> None:
    # given
    name = "label1"
    color = "#FF00AA"

    # when
    label = DeviceLabel(name=name, color=color)

    # then
    assert label.name == name
    assert label.color == color


def test_update_constructor_success() -> None:
    # given
    id = ID(100)
    name = "label1"
    color = "#FF00AA"

    # when
    label = DeviceLabel(id=id, name=name, color=color)

    # then
    assert label.id == id
    assert label.name == name
    assert label.color == color


def test_internal_constructor_success() -> None:
    # given
    name = "label1"
    color = "#FF00AA"
    id = ID(100)
    user_id = ID(300)
    company_id = ID(700)
    device = DeviceItem(id=ID(20), device_name="device1", device_subtype="aws", device_type="router")
    created_date = "1970"
    updated_date = "1971"

    # when
    label = DeviceLabel(
        name=name,
        color=color,
        devices=[device],
        id=id,
        user_id=user_id,
        company_id=company_id,
        created_date=created_date,
        updated_date=updated_date,
    )

    # then
    assert label.name == name
    assert label.color == color
    assert label.id == id
    assert label.user_id == user_id
    assert label.company_id == company_id
    assert len(label.devices) == 1
    assert label.devices[0] == device
    assert label.created_date == created_date
