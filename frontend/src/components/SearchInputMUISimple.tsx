/**
 * Simplified Material-UI search input with city autocomplete
 * Uses Google Places API for city suggestions
 */

import { useState, useEffect, useCallback } from 'react';
import { styled } from '@mui/material/styles';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import { MagnifyingGlassIcon, MapPinIcon } from '@heroicons/react/24/solid';
import { useLazyQuery } from '@apollo/client';
import { CITY_AUTOCOMPLETE } from '../graphql/queries';
import debounce from 'lodash/debounce';

interface CitySuggestion {
  placeId: string;
  description: string;
  mainText: string;
  secondaryText: string;
}

interface SearchInputMUISimpleProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  placeholder?: string;
  autoFocus?: boolean;
  className?: string;
}

// Custom styled components to match Tailwind design
const StyledAutocomplete = styled(Autocomplete)(() => ({
  '& .MuiOutlinedInput-root': {
    borderRadius: '0.5rem',
    backgroundColor: 'white',
    '&:hover .MuiOutlinedInput-notchedOutline': {
      borderColor: '#3b82f6',
    },
    '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
      borderColor: '#3b82f6',
      borderWidth: '2px',
    },
  },
  '& .MuiAutocomplete-inputRoot': {
    paddingLeft: '0.75rem',
  },
}));

export const SearchInputMUISimple: React.FC<SearchInputMUISimpleProps> = ({
  value,
  onChange,
  onSubmit,
  placeholder = "Enter city name",
  autoFocus = false,
  className = "",
}) => {
  const [inputValue, setInputValue] = useState(value);
  const [options, setOptions] = useState<CitySuggestion[]>([]);

  const [getCityAutocomplete, { loading: autocompleteLoading }] = useLazyQuery(
    CITY_AUTOCOMPLETE,
    {
      onCompleted: (data) => {
        setOptions(data?.cityAutocomplete || []);
      },
    }
  );

  // Debounced function to fetch city suggestions
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const fetchCitySuggestions = useCallback(
    debounce((input: string) => {
      // Skip if input is too short
      if (!input || input.trim().length < 2) {
        setOptions([]);
        return;
      }

      // Fetch city suggestions
      getCityAutocomplete({
        variables: {
          inputText: input,
          country: 'us',
        },
      });
    }, 300),
    [getCityAutocomplete]
  );

  // Update options when input changes
  useEffect(() => {
    fetchCitySuggestions(inputValue);
  }, [inputValue, fetchCitySuggestions]);

  // Update input value when external value changes
  useEffect(() => {
    setInputValue(value);
  }, [value]);

  return (
    <StyledAutocomplete
      freeSolo
      value={value}
      onChange={(_event, newValue) => {
        if (typeof newValue === 'string') {
          onChange(newValue);
        } else if (newValue && typeof newValue === 'object' && 'mainText' in newValue) {
          const suggestion = newValue as CitySuggestion;
          onChange(suggestion.mainText);
          setTimeout(() => onSubmit(), 100);
        }
      }}
      inputValue={inputValue}
      onInputChange={(_event, newInputValue) => {
        setInputValue(newInputValue);
        onChange(newInputValue);
      }}
      options={options}
      loading={autocompleteLoading}
      autoHighlight
      filterOptions={(x) => x}
      getOptionLabel={(option) => {
        if (typeof option === 'string') {
          return option;
        }
        return (option as CitySuggestion).mainText || '';
      }}
      renderOption={(props, option) => (
        <li {...props} className="flex items-start space-x-3 px-4 py-3 hover:bg-gray-50">
          <MapPinIcon className="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" />
          <div className="flex-1">
            <div className="font-medium text-gray-900">
              {(option as CitySuggestion).mainText}
            </div>
            {(option as CitySuggestion).secondaryText && (
              <div className="text-sm text-gray-500">
                {(option as CitySuggestion).secondaryText}
              </div>
            )}
          </div>
        </li>
      )}
      renderInput={(params) => (
        <TextField
          {...params}
          placeholder={placeholder}
          autoFocus={autoFocus}
          className={className}
          InputProps={{
            ...params.InputProps,
            startAdornment: (
              <InputAdornment position="start">
                <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
              </InputAdornment>
            ),
          }}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              e.preventDefault();
              onSubmit();
            }
          }}
        />
      )}
    />
  );
};
