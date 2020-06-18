# Backend Routes

1. Users:

   - POST "/users"
     - This endpoint will create a new user
   - GET "/users/:user_id/songs"
   - This enpoint will get all the songs for a specific user

2. Songs:

   - GET "/songs"
     - This endpoint returns all songs
   - GET "/songs/:song_id"
     - This endpoint returns all info for a single song @id
   - POST "/songs"
     - This endpoint will create a new song
   - PUT "/songs/:song_id"
     - This endpoint will update a song @id
   - DELETE "/songs/:song_id"
     - This endpoint will delete a song @id

3. Favorites:
   - POST "/songs/:id/favorite"
     - This endpoint adds a favorite to song @id
   - DELETE "/songs/:id/favorite"
     - This endpoint removes a favorite to set @id for logged in user
