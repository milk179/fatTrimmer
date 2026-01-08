.........................................................................................
Andre Morgan
1/7/2026

Setup steps:

    Log into Spotify for Developers with your Spotify account
        Go to your dashboard
        Click on create app

        For website put: http://localhost
        For Redirect URIs put: http://127.0.0.1:8888/callback

    Open Terminal and run

        export SPOTIPY_CLIENT_ID='your-spotify-client-id'
        export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
        export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

    Instead, if using Windows open Powershell and run

        $env:SPOTIPY_CLIENT_ID="your-spotify-client-id"
        $env:SPOTIPY_CLIENT_SECRET="your-spotify-client-secret"
        $env:SPOTIPY_REDIRECT_URI="your-app-redirect-url"