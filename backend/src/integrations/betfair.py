"""Betfair Adapter - REAL API CALLS"""
from src.integrations.base import ProviderAdapter, ProviderConfig
from typing import Any, Dict, Optional
import logging
from datetime import datetime, timedelta
import requests
import json

logger = logging.getLogger(__name__)

class BetfairAdapter(ProviderAdapter):
    """Betfair Exchange API - Real connections only"""
    
    LOGIN_URL = "https://identitysso.betfair.com/api/login"
    API_URL = "https://api.betfair.com/exchange/betting/json-rpc/v1"
    HORSE_RACING_EVENT_TYPE_ID = "7"
    
    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.api_key: Optional[str] = None
        self.session_token: Optional[str] = None
        self.session_expiry: Optional[datetime] = None
    
    async def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """Non-interactive login to Betfair API"""
        try:
            self.username = credentials.get("username")
            self.password = credentials.get("password")
            self.api_key = credentials.get("api_key")
            
            if not all([self.username, self.password, self.api_key]):
                logger.error("Missing credentials: username, password, api_key required")
                return False
            
            login_payload = {
                "username": self.username,
                "password": self.password
            }
            
            headers = {
                "X-Application": self.api_key,
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            response = requests.post(
                self.LOGIN_URL,
                data=login_payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.session_token = result.get("sessionToken")
                self.session_expiry = datetime.utcnow() + timedelta(hours=12)
                self.is_authenticated = True
                logger.info(f"✅ Betfair authenticated: {self.config.name}")
                return True
            else:
                logger.error(f"❌ Betfair login failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Betfair auth error: {e}")
            return False
    
    def _make_api_call(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make JSON-RPC call to Betfair API"""
        if not self.is_authenticated or not self.session_token:
            raise Exception("Not authenticated")
        
        headers = {
            "X-Application": self.api_key,
            "X-Authentication": self.session_token,
            "Content-Type": "application/json"
        }
        
        payload = {
            "jsonrpc": "2.0",
            "method": f"SportsAPING/v1.0/{method}",
            "params": params,
            "id": 1
        }
        
        try:
            response = requests.post(
                self.API_URL,
                data=json.dumps(payload),
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if "result" in result:
                    return result["result"]
                else:
                    logger.error(f"API error: {result}")
                    return {}
            else:
                logger.error(f"API failed: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"API call error: {e}")
            return {}
    
    async def fetch_raw_data(self, **kwargs) -> Dict[str, Any]:
        """Fetch horse racing markets with runners and prices"""
        if not self.is_authenticated:
            raise Exception("Not authenticated")
        
        try:
            now = datetime.utcnow()
            
            # Get events
            events = self._make_api_call("listEvents", {
                "filter": {
                    "eventTypeIds": [self.HORSE_RACING_EVENT_TYPE_ID],
                    "marketTime": {
                        "from": now.isoformat() + "Z",
                        "to": (now + timedelta(hours=24)).isoformat() + "Z"
                    }
                }
            })
            
            if not events:
                return {"events": [], "markets": [], "prices": []}
            
            # Get markets
            event_ids = [e["event"]["id"] for e in events]
            markets = self._make_api_call("listMarketCatalogue", {
                "filter": {
                    "eventIds": event_ids,
                    "marketTypes": ["WIN", "PLACE"]
                },
                "maxResults": "1000",
                "marketProjections": ["RUNNER_DESCRIPTION", "MARKET_DESCRIPTION"]
            })
            
            if not markets:
                return {"events": events, "markets": [], "prices": []}
            
            # Get prices
            market_ids = [m["marketId"] for m in markets]
            prices = self._make_api_call("listMarketBook", {
                "marketIds": market_ids,
                "priceProjection": {
                    "priceData": ["EX_BEST_OFFERS", "EX_TRADED"]
                }
            })
            
            logger.info(f"✅ Fetched {len(markets)} Betfair markets")
            
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "events": events,
                "markets": markets,
                "prices": prices,
                "total_markets": len(markets)
            }
            
        except Exception as e:
            logger.error(f"❌ Fetch error: {e}")
            return {"error": str(e)}
    
    async def validate_connection(self) -> bool:
        """Test API connection"""
        try:
            result = self._make_api_call("listEventTypes", {"filter": {}})
            return len(result) > 0
        except Exception as e:
            logger.error(f"❌ Connection test failed: {e}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Check provider health"""
        try:
            is_valid = await self.validate_connection()
            return {
                "status": "healthy" if is_valid else "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "provider": "betfair",
                "authenticated": self.is_authenticated
            }
        except Exception as e:
            logger.error(f"❌ Health check error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def get_provider_schema(self) -> Dict[str, Any]:
        """Return Betfair schema"""
        return {
            "events": "array",
            "markets": "array",
            "prices": "array",
            "timestamp": "ISO8601"
        }
