from datetime import date, timedelta

from expects import expect, equal, have_len, raise_error

from specs.helpers.mamba_keywords import description, context, it
from src.model.auction.auction import Auction
from src.model.auction.auction_error import AuctionError


def auction_with(price, expiration_date=date.max):
    return Auction.create(auction_id='an_auction_id', auctioneer='an_auctioneer_id', item='an_item_id',
                          expiration_date=expiration_date, selling_price=price)


with description('Auction'):
    with context('on creation success'):
        with it('produces an event of auction created'):
            price = 600
            auction = auction_with(price=price, expiration_date=date.today())

            expect(auction.events).to(have_len(1))
            expect(auction.events[0]).to(equal({
                'type': Auction.AUCTION_CREATED_TYPE,
                'auction_id': 'an_auction_id',
                'auctioneer': 'an_auctioneer_id',
                'item': 'an_item_id',
                'expiration_date': date.today().isoformat(),
                'selling_price': price
            }))

    with context('on invariants failed'):
        with it('does not allow the creation when selling price is less than 1'):
            auction = lambda: auction_with(price=0)

            expect(auction).to(raise_error(AuctionError, 'selling price must be greater than 1'))

        with it('does not allow the creation when expiration date is before today'):
            yesterday = date.today() - timedelta(days=1)
            auction = lambda: auction_with(price=600, expiration_date=yesterday)

            expect(auction).to(raise_error(AuctionError, 'expiration date cannot be before today'))