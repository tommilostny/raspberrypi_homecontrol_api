using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Colors
{
    public class ColorDbService
    {
        private readonly HttpClient _httpClient;

        public ColorDbService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<ColorModel>> GetColorDb()
        {
            var response = await _httpClient.GetAsync($"colors");
            var content = await response.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<List<ColorModel>>(content);
        }
    }
}
