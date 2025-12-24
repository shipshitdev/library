---
name: React Native Components
title: React Native Component Patterns Expert
description: Master React Native 0.79.5 components, styling, performance optimization, and mobile UI best practices with real-world examples
category: mobile
tags: [react-native, components, styling, performance, ui, accessibility, hooks]
version: 1.0.0
difficulty: advanced
---

# React Native Component Patterns Expert

**You are an expert in React Native 0.79.5 component architecture, StyleSheet patterns, performance optimization, and mobile-first UI development with a focus on clean, maintainable, and accessible code.**

## Core Components

### View - The Foundation

`View` is the fundamental container component, equivalent to `div` in web.

```tsx
import { View, StyleSheet } from 'react-native';

export default function Container() {
  return (
    <View style={styles.container}>
      <View style={styles.card}>
        {/* Content */}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
    padding: 24,
  },
  card: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 16,
    // Flexbox is default
    flexDirection: 'row',
    gap: 16,
  },
});
```

**Key Properties**:
- Flexbox by default (`display: 'flex'` implicit)
- No `gap` support on older RN versions (0.79+ has it)
- Use `pointerEvents` to control touch handling

### Text - Typography

All text must be wrapped in `Text` component (unlike web).

```tsx
import { Text, StyleSheet } from 'react-native';

export default function Typography() {
  return (
    <>
      <Text style={styles.title}>
        Product Title
      </Text>
      <Text style={styles.description} numberOfLines={2}>
        Long description that will be truncated after two lines with ellipsis...
      </Text>
      <Text style={styles.meta}>
        2 hours ago
      </Text>
    </>
  );
}

const styles = StyleSheet.create({
  title: {
    fontSize: 24,
    fontWeight: '600',
    color: 'white',
    letterSpacing: -0.5,
  },
  description: {
    fontSize: 15,
    lineHeight: 22,
    color: '#cbd5f5',
  },
  meta: {
    fontSize: 13,
    color: '#94a3b8',
  },
});
```

**Key Properties**:
- `numberOfLines` - Truncate with ellipsis
- `ellipsizeMode` - 'head' | 'middle' | 'tail' | 'clip'
- `selectable` - Allow text selection
- Font weights: '100'-'900' or 'normal' | 'bold'

### Image - Asset Loading

Use `expo-image` for optimized images (faster, better caching).

```tsx
import { Image } from 'expo-image';
import { StyleSheet } from 'react-native';

export default function ImageExamples() {
  return (
    <>
      {/* Remote image with caching */}
      <Image
        source={{ uri: 'https://example.com/image.jpg' }}
        style={styles.thumbnail}
        contentFit="cover"
        transition={200}
        cachePolicy="memory-disk"
      />

      {/* Local asset */}
      <Image
        source={require('@/assets/images/logo.png')}
        style={styles.logo}
        contentFit="contain"
      />
    </>
  );
}

const styles = StyleSheet.create({
  thumbnail: {
    width: 128,
    height: 72,
    borderRadius: 12,
  },
  logo: {
    width: 100,
    height: 100,
  },
});
```

**expo-image Benefits**:
- Better performance than RN Image
- Built-in caching (`memory`, `disk`, `memory-disk`)
- Smooth transitions
- `contentFit`: 'cover' | 'contain' | 'fill' | 'none' | 'scale-down'

### ScrollView - Scrollable Content

```tsx
import { ScrollView, View, StyleSheet } from 'react-native';

export default function Content() {
  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.contentContainer}
      showsVerticalScrollIndicator={false}
    >
      {/* Content */}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,  // Applied to ScrollView itself
  },
  contentContainer: {
    padding: 24,
    paddingBottom: 48,
    gap: 32,
  },
});
```

**Key Properties**:
- `style` - Applied to container
- `contentContainerStyle` - Applied to scrollable content
- `showsVerticalScrollIndicator` - Hide scroll indicator
- `bounces` (iOS) - Enable/disable bounce effect

## StyleSheet Patterns

### 1. StyleSheet.create - Performance Optimized

```tsx
import { StyleSheet, View, Text } from 'react-native';

// From actual codebase: app/(protected)/content.tsx
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
  },
  contentContainer: {
    padding: 24,
    paddingBottom: 48,
    gap: 32,
  },
  card: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 16,
    flexDirection: 'row',
    gap: 16,
  },
  videoThumbnail: {
    width: 128,
    height: 72,
    borderRadius: 12,
  },
  cardTitle: {
    color: 'white',
    fontSize: 17,
    fontWeight: '600',
  },
  cardMeta: {
    color: '#94a3b8',
    fontSize: 13,
  },
});
```

**Benefits**:
- Validates style properties at creation
- Better performance (styles are stored by ID)
- Works with React DevTools

### 2. Dynamic Styles - Conditional Styling

```tsx
import { StyleSheet, TouchableOpacity, Text } from 'react-native';

// From actual codebase: app/(protected)/ideas.tsx
function TypePill({
  label,
  isActive,
  onPress,
}: {
  label: string;
  isActive: boolean;
  onPress: () => void;
}) {
  return (
    <TouchableOpacity
      onPress={onPress}
      style={[
        styles.typePill,
        isActive ? styles.typePillActive : styles.typePillInactive,
      ]}
    >
      <Text style={[styles.typePillLabel, isActive && styles.typePillLabelActive]}>
        {label}
      </Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  typePill: {
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 999,
    borderWidth: 1,
  },
  typePillInactive: {
    borderColor: '#1e293b',
    backgroundColor: '#0f172a',
  },
  typePillActive: {
    borderColor: '#38bdf8',
    backgroundColor: 'rgba(56, 189, 248, 0.16)',
  },
  typePillLabel: {
    color: '#94a3b8',
    fontSize: 14,
    fontWeight: '500',
  },
  typePillLabelActive: {
    color: '#e0f2fe',
  },
});
```

**Array Syntax**:
- Styles are applied left to right
- Later styles override earlier ones
- `false` | `null` | `undefined` are ignored
- Pattern: `[baseStyle, condition && conditionalStyle]`

### 3. Responsive Design

```tsx
import { StyleSheet, Dimensions, Platform } from 'react-native';

const { width, height } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    padding: width > 768 ? 32 : 24,  // Tablet vs phone
  },
  card: {
    width: width > 768 ? '50%' : '100%',
  },
});

// Listen for dimension changes
import { useWindowDimensions } from 'react-native';

function ResponsiveComponent() {
  const { width } = useWindowDimensions();
  const isTablet = width > 768;

  return (
    <View style={[styles.container, { padding: isTablet ? 32 : 24 }]}>
      {/* Content */}
    </View>
  );
}
```

### 4. Platform-Specific Styling

```tsx
import { StyleSheet, Platform } from 'react-native';

const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.select({
      ios: 20,
      android: 25,
      web: 0,
    }),
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
      },
      android: {
        elevation: 4,
      },
    }),
  },
});
```

## Real-World Component Patterns

### 1. Card Component (Production Example)

From `app/(protected)/content.tsx`:

```tsx
import { View, Text, Image, StyleSheet } from 'react-native';

interface VideoCardProps {
  item: {
    id: string;
    title: string;
    description: string;
    thumbnail: string;
    createdAt: string;
    stats: string;
  };
}

function VideoCard({ item }: VideoCardProps) {
  return (
    <View style={styles.card}>
      <Image source={{ uri: item.thumbnail }} style={styles.videoThumbnail} />
      <View style={styles.cardBody}>
        <Text style={styles.cardTitle}>{item.title}</Text>
        <Text style={styles.cardMeta}>{item.createdAt}</Text>
        <Text style={styles.cardDescription}>{item.description}</Text>
        <Text style={styles.cardFootnote}>{item.stats}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#1e293b',
    borderRadius: 16,
    padding: 16,
    flexDirection: 'row',
    gap: 16,
  },
  videoThumbnail: {
    width: 128,
    height: 72,
    borderRadius: 12,
  },
  cardBody: {
    flex: 1,
    gap: 6,
  },
  cardTitle: {
    color: 'white',
    fontSize: 17,
    fontWeight: '600',
  },
  cardMeta: {
    color: '#94a3b8',
    fontSize: 13,
  },
  cardDescription: {
    color: '#cbd5f5',
    fontSize: 14,
    lineHeight: 20,
  },
  cardFootnote: {
    color: '#94a3b8',
    fontSize: 12,
  },
});
```

**Key Patterns**:
- `flexDirection: 'row'` for horizontal layout
- `flex: 1` on cardBody to fill remaining space
- `gap` for consistent spacing (RN 0.79+)
- TypeScript interfaces for props
- Semantic color naming

### 2. Input Component (Production Example)

From `app/(protected)/ideas.tsx`:

```tsx
import { TextInput, StyleSheet } from 'react-native';

function Input() {
  const [value, setValue] = useState('');

  return (
    <TextInput
      value={value}
      onChangeText={setValue}
      placeholder="What should we ideate around?"
      placeholderTextColor="#64748b"
      style={styles.input}
      autoCapitalize="none"
      autoCorrect={false}
    />
  );
}

const styles = StyleSheet.create({
  input: {
    borderWidth: 1,
    borderColor: '#1e293b',
    borderRadius: 14,
    paddingHorizontal: 16,
    paddingVertical: 12,
    color: 'white',
    fontSize: 15,
    backgroundColor: '#020617',
  },
  inputMultiline: {
    minHeight: 80,
    textAlignVertical: 'top',
  },
});
```

**Key Properties**:
- `placeholderTextColor` - Always set (default is invisible on dark backgrounds)
- `autoCapitalize` - 'none' | 'sentences' | 'words' | 'characters'
- `autoCorrect` - Disable for usernames, emails
- `multiline` - Multi-line input
- `textAlignVertical: 'top'` - Align text to top in multiline

### 3. Button Component (Production Example)

From `app/(protected)/ideas.tsx`:

```tsx
import { TouchableOpacity, Text, StyleSheet } from 'react-native';

interface ButtonProps {
  onPress: () => void;
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
}

function Button({ onPress, children, variant = 'primary' }: ButtonProps) {
  return (
    <TouchableOpacity
      style={[styles.button, styles[`button${variant}`]]}
      onPress={onPress}
      activeOpacity={0.8}
    >
      <Text style={styles.buttonLabel}>{children}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    borderRadius: 16,
    alignItems: 'center',
    paddingVertical: 14,
    marginTop: 8,
  },
  buttonPrimary: {
    backgroundColor: '#38bdf8',
  },
  buttonSecondary: {
    backgroundColor: '#1e293b',
    borderWidth: 1,
    borderColor: '#38bdf8',
  },
  buttonLabel: {
    color: '#0f172a',
    fontSize: 15,
    fontWeight: '600',
  },
});
```

**Touchable Components**:
- `TouchableOpacity` - Reduces opacity on press
- `TouchableHighlight` - Shows highlight color
- `TouchableWithoutFeedback` - No visual feedback
- `Pressable` - Modern, more configurable (recommended)

### 4. Section Header (Production Example)

From `app/(protected)/content.tsx`:

```tsx
import { View, Text, StyleSheet } from 'react-native';

function SectionHeader({ label }: { label: string }) {
  return (
    <View style={styles.sectionHeader}>
      <Text style={styles.sectionLabel}>{label}</Text>
      <Text style={styles.sectionAction}>View all</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  sectionLabel: {
    color: 'white',
    fontSize: 18,
    fontWeight: '600',
  },
  sectionAction: {
    color: '#38bdf8',
    fontSize: 14,
    fontWeight: '500',
  },
});
```

## Performance Optimization

### 1. FlatList for Long Lists

```tsx
import { FlatList, View, Text, StyleSheet } from 'react-native';

interface Item {
  id: string;
  title: string;
}

function OptimizedList({ data }: { data: Item[] }) {
  const renderItem = ({ item }: { item: Item }) => (
    <View style={styles.item}>
      <Text>{item.title}</Text>
    </View>
  );

  return (
    <FlatList
      data={data}
      renderItem={renderItem}
      keyExtractor={(item) => item.id}
      // Performance optimizations
      initialNumToRender={10}
      maxToRenderPerBatch={10}
      windowSize={5}
      removeClippedSubviews={true}
      // Visual improvements
      showsVerticalScrollIndicator={false}
      contentContainerStyle={styles.listContent}
    />
  );
}

const styles = StyleSheet.create({
  listContent: {
    padding: 24,
    gap: 16,
  },
  item: {
    padding: 16,
    backgroundColor: '#1e293b',
    borderRadius: 12,
  },
});
```

**Key Properties**:
- `initialNumToRender` - Number of items to render initially
- `maxToRenderPerBatch` - Batch size for rendering
- `windowSize` - Number of screen heights to render
- `removeClippedSubviews` - Unmount off-screen views
- `getItemLayout` - Skip measurement if items have fixed height

### 2. React.memo for Components

```tsx
import { memo } from 'react';
import { View, Text } from 'react-native';

interface CardProps {
  title: string;
  description: string;
}

const Card = memo(({ title, description }: CardProps) => {
  return (
    <View style={styles.card}>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.description}>{description}</Text>
    </View>
  );
});
```

### 3. useMemo for Expensive Computations

From `app/(protected)/ideas.tsx`:

```tsx
import { useMemo } from 'react';

function Ideas({ selectedType }: { selectedType: string }) {
  const generatedLabel = useMemo(
    () => `${selectedType.charAt(0).toUpperCase() + selectedType.slice(1)} ideas ready to pitch`,
    [selectedType],
  );

  return <Text>{generatedLabel}</Text>;
}
```

### 4. useCallback for Event Handlers

```tsx
import { useCallback } from 'react';
import { TouchableOpacity } from 'react-native';

function ButtonList({ items }: { items: string[] }) {
  const handlePress = useCallback((id: string) => {
    console.log('Pressed:', id);
  }, []);

  return (
    <>
      {items.map((item) => (
        <TouchableOpacity key={item} onPress={() => handlePress(item)}>
          <Text>{item}</Text>
        </TouchableOpacity>
      ))}
    </>
  );
}
```

## Custom Hooks

### 1. useWindowDimensions Hook

```tsx
import { useWindowDimensions } from 'react-native';

function ResponsiveComponent() {
  const { width, height, scale, fontScale } = useWindowDimensions();
  const isTablet = width > 768;

  return (
    <View style={{ padding: isTablet ? 32 : 24 }}>
      <Text>Width: {width}</Text>
    </View>
  );
}
```

### 2. Custom Hook for Form State

```tsx
import { useState, useCallback } from 'react';

interface FormValues {
  [key: string]: string;
}

function useForm(initialValues: FormValues) {
  const [values, setValues] = useState(initialValues);

  const handleChange = useCallback((field: string, value: string) => {
    setValues((prev) => ({ ...prev, [field]: value }));
  }, []);

  const reset = useCallback(() => {
    setValues(initialValues);
  }, [initialValues]);

  return { values, handleChange, reset };
}

// Usage
function LoginForm() {
  const { values, handleChange } = useForm({ email: '', password: '' });

  return (
    <>
      <TextInput
        value={values.email}
        onChangeText={(text) => handleChange('email', text)}
      />
      <TextInput
        value={values.password}
        onChangeText={(text) => handleChange('password', text)}
        secureTextEntry
      />
    </>
  );
}
```

## Accessibility

### 1. Screen Reader Support

```tsx
import { View, Text, TouchableOpacity } from 'react-native';

function AccessibleButton() {
  return (
    <TouchableOpacity
      accessible={true}
      accessibilityLabel="Close dialog"
      accessibilityHint="Dismisses the current screen"
      accessibilityRole="button"
      onPress={() => {}}
    >
      <Text>×</Text>
    </TouchableOpacity>
  );
}
```

**Key Properties**:
- `accessible` - Enable accessibility
- `accessibilityLabel` - Screen reader description
- `accessibilityHint` - Additional context
- `accessibilityRole` - Semantic role
- `accessibilityState` - Current state (disabled, selected, etc.)

### 2. Accessibility Roles

Common roles:
- `button` - Buttons
- `header` - Section headers
- `link` - Links
- `image` - Images
- `text` - Text content
- `search` - Search inputs

### 3. Focus Management

```tsx
import { useRef } from 'react';
import { TextInput } from 'react-native';

function LoginForm() {
  const passwordRef = useRef<TextInput>(null);

  return (
    <>
      <TextInput
        placeholder="Email"
        returnKeyType="next"
        onSubmitEditing={() => passwordRef.current?.focus()}
      />
      <TextInput
        ref={passwordRef}
        placeholder="Password"
        returnKeyType="done"
        secureTextEntry
      />
    </>
  );
}
```

## Layout Patterns

### 1. Flexbox (Default)

```tsx
const styles = StyleSheet.create({
  // Column layout (default)
  column: {
    flexDirection: 'column',  // default
    gap: 16,
  },
  // Row layout
  row: {
    flexDirection: 'row',
    gap: 16,
    alignItems: 'center',
  },
  // Space between
  spaceBetween: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  // Centered
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
```

### 2. Absolute Positioning

```tsx
const styles = StyleSheet.create({
  container: {
    position: 'relative',
    width: 300,
    height: 200,
  },
  badge: {
    position: 'absolute',
    top: 8,
    right: 8,
    backgroundColor: '#38bdf8',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
});
```

## Advanced Patterns

### 1. Compound Components

```tsx
interface TabsContextValue {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function Tabs({ children }: { children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState('video');

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  );
}

function TabButton({ value, children }: { value: string; children: React.ReactNode }) {
  const context = useContext(TabsContext);
  const isActive = context?.activeTab === value;

  return (
    <TouchableOpacity onPress={() => context?.setActiveTab(value)}>
      <Text style={[styles.tab, isActive && styles.tabActive]}>
        {children}
      </Text>
    </TouchableOpacity>
  );
}

// Usage
<Tabs>
  <TabButton value="video">Video</TabButton>
  <TabButton value="image">Image</TabButton>
</Tabs>
```

### 2. Render Props Pattern

```tsx
interface LoadingProps<T> {
  isLoading: boolean;
  data: T | null;
  error: Error | null;
  children: (data: T) => React.ReactNode;
}

function Loading<T>({ isLoading, data, error, children }: LoadingProps<T>) {
  if (isLoading) return <Text>Loading...</Text>;
  if (error) return <Text>Error: {error.message}</Text>;
  if (!data) return null;

  return <>{children(data)}</>;
}

// Usage
<Loading isLoading={loading} data={user} error={error}>
  {(user) => <Text>{user.name}</Text>}
</Loading>
```

## Best Practices

### 1. Component Structure
- Keep components small and focused
- Extract reusable components early
- Use TypeScript for all props
- Colocate styles with components

### 2. Performance
- Use `FlatList` for lists > 50 items
- Memoize expensive computations with `useMemo`
- Memoize callbacks with `useCallback`
- Use `React.memo` for pure components
- Avoid inline functions in render

### 3. Styling
- Use `StyleSheet.create` for better performance
- Define styles outside component (unless dynamic)
- Use semantic color variables
- Keep platform-specific code minimal

### 4. Accessibility
- Add `accessibilityLabel` to all interactive elements
- Use correct `accessibilityRole`
- Support screen readers
- Test with VoiceOver (iOS) and TalkBack (Android)

### 5. TypeScript
- Define interfaces for all component props
- Use discriminated unions for variants
- Avoid `any` type
- Leverage inference where possible

## Summary

You are now equipped to:
- Build performant React Native components
- Style with StyleSheet and handle platform differences
- Optimize rendering with FlatList, memo, useMemo
- Create accessible mobile interfaces
- Implement custom hooks for reusable logic
- Apply advanced patterns like compound components
- Follow mobile-first best practices

Always prioritize:
1. Performance (FlatList, memoization)
2. Accessibility (screen readers, semantic HTML)
3. Type safety (TypeScript strict mode)
4. Clean, maintainable code
5. Responsive design for all screen sizes
